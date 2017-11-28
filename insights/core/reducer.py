import logging
import os
import sys
import time
from collections import defaultdict

from insights.config.static import get_config
from insights.contrib import toposort
from insights.core import marshalling, plugins, get_name, SkipComponent
from insights.util import logging_level

specs = get_config()
logger = logging.getLogger("reducer")
marshaller = marshalling.Marshaller()


def pattern_file(symbolic_name):
    return specs.is_multi_output(symbolic_name)


def autobox(symbolic_names, output):
    if pattern_file(symbolic_names[0]):
        return marshaller.unmarshal_to_context(output)
    elif len(output) > 1:
        logger.warning("Simple file [%s] has multiple returns", symbolic_names[0])
    return output[0]


def collect_results(results_dict):
    plugin_output = defaultdict(dict)
    shared_output = {}
    for producer, output in results_dict.iteritems():
        if producer.shared:
            if not producer._reducer:
                is_pattern = pattern_file(producer.symbolic_names[0])
                shared_output[producer] = output if is_pattern else output[0]
            else:
                shared_output[producer] = output
        else:
            plugin = sys.modules[producer.__module__]
            plugin_output[plugin].update(autobox(producer.symbolic_names, output))
    return plugin_output, shared_output


def collect_results_multi(results_dict):
    combined_local_output = defaultdict(lambda: defaultdict(list))
    combined_shared_output = defaultdict(dict)
    for host, results_dict in results_dict.iteritems():
        plugin_output, shared_output = collect_results(results_dict)
        for plugin, output in plugin_output.iteritems():
            for k, v in output.iteritems():
                combined_local_output[plugin][k].append(v)
        for parser, output in shared_output.iteritems():
            combined_shared_output[parser][host] = output
    return combined_local_output, combined_shared_output


def run_multi(parser_output, all_output, error_handler, reducers=plugins.CLUSTER_REDUCERS, reducer_stats=None, ):
    logger.debug("Multi-node reducer run started")
    if reducers != plugins.CLUSTER_REDUCERS:
        log_reducers(reducers)
    plugin_output, shared_output = collect_results_multi(parser_output)
    for func, r in _run(reducers, plugin_output, shared_output, error_handler, reducer_stats=reducer_stats):
        yield func, r
    all_output.update(parser_output)
    all_output.update(shared_output)


def run(parser_output, error_handler):
    logger.debug("Batch-mode reducer run started")
    for host, parser_dict in parser_output.iteritems():
        for func, r in run_host(parser_dict, {}, error_handler):
            yield host, func, r


def run_host(parser_dict, all_output, error_handler, reducers=plugins.REDUCERS, reducer_stats=None):
    logger.debug("Single-node reducer run started")
    if reducers != plugins.REDUCERS:
        log_reducers(reducers)
    local_output, shared_output = collect_results(parser_dict)

    all_output.update(parser_dict)
    for func, r in _run(reducers, local_output, shared_output, error_handler,
                        output_dict=parser_dict, reducer_stats=reducer_stats):
        yield func, r
    items = list(default_reducer_results(local_output))
#    for func, r in default_reducer_results(local_output):
#        yield func, r
    all_output.update(shared_output)
    all_output.update(dict(items))
    for func, r in items:
        yield func, r


@logging_level(logger, logging.DEBUG)
def log_reducers(reducers):
    logger.debug("Custom reducer listing:")
    for reducer in sorted(reducers.values()):
        logger.debug("\t" + reducer.serializable_id)


@logging_level(logger, logging.DEBUG)
def log_parser_outputs(func, local_output, shared_output):
    logger.debug("Invoking reducer [%s]", func.serializable_id)
    logger.debug("\tLocal keys: %s", sorted(local_output.keys()))
    if len(shared_output) > 0 and hasattr(shared_output.keys()[0], "serializable_id"):
        parser_outputs = [o.serializable_id for o in sorted(shared_output.keys())]
    else:
        parser_outputs = [o for o in sorted(shared_output.keys())]
    logger.debug("\tShared parser outputs: %s", parser_outputs)


def run_order(components):
    """ Returns components in the order they should be run so that
        dependencies among components are met.
    """

    graph = {}
    for c in components:
        graph.update(plugins.get_dependency_graph(c))
    ordered = toposort.toposort_flatten(graph)
    return [o for o in ordered if o._reducer]


def _run(reducers, local_output, shared_output, error_handler, output_dict=None, reducer_stats=None):
    clustered = any(r.cluster for r in reducers.values())
    for func in run_order(reducers.values()):

        # if a cluster reducer depends on a regular shared reducer, that
        # shared reducer will already have run in a sub evaluator
        # and been shifted to the top of this dict. Don't try to
        # run it again in a clustered context.
        if clustered and func.shared and not func.cluster:
            continue
        real_module = sys.modules[func.__module__]
        local = local_output[real_module]
        log_parser_outputs(func, local, shared_output)
        if func not in shared_output:
            r = run_reducer(func, local, shared_output, error_handler, reducer_stats=reducer_stats)
            if r is not None:
                shared_output[func] = r
                logger.debug("Reducer output: %s", r)
                if func.shared and output_dict:
                    output_dict[func] = r
                if func in plugins.EMITTERS:
                    yield func, r


def default_reducer_results(local_output):
    for module, output in local_output.iteritems():
        if "type" in output and output["type"] in ["metadata", "rule"]:
            yield plugins.PLUGINS[module.__name__]["parsers"][0], output


def run_reducer(func, local, shared, error_handler, reducer_stats=None):
    start = time.time()
    try:
        r = plugins.DELEGATES[func](local, shared)
        if reducer_stats:
            reducer_stats['count'] += 1
        return r
    except SkipComponent as sc:
        logger.debug("Skipping reducer %s: %s" % (str(func), str(sc)))
        return None
    except Exception as e:
        if reducer_stats:
            reducer_stats['fail'] += 1
        error_handler(func, e, local, shared)
    finally:
        elapsed = time.time() - start
        if elapsed > float(os.environ.get("SLOW_COMPONENT_THRESHOLD", 1)):
            logger.warning("Reducer %s took %.2f seconds to execute.", get_name(func), elapsed, extra={
                "reducer": get_name(func),
                "elapsed": elapsed
            })
