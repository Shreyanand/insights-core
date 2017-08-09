from insights.tools import generate_api_config
from insights.parsers import *  # noqa


def latest():
    return generate_api_config.APIConfigGenerator(plugin_package="insights.tests.test_plugins").serialize_data_spec()


def test_top_level():
    # these sections must exist and not be empty
    for each in ['version', 'files', 'commands', 'specs', 'pre_commands', 'meta_specs']:
        assert each in latest
        assert len(latest[each]) > 0


def test_meta_specs():
    # these sections must exist in the meta_specs, have a 'archive_file_name' field,
    #   and it must not be empty
    for each in ['analysis_target', 'branch_info', 'machine-id', 'uploader_log']:
        assert each in latest['meta_specs']
        assert 'archive_file_name' in latest['meta_specs'][each]
        assert len(latest['meta_specs'][each]['archive_file_name']) > 0


def test_specs():
    # check that each spec only has target sections for known targets
    for eachspec in latest['specs']:
        for eachtarget in latest['specs'][eachspec]:
            assert eachtarget in ['host', 'docker_container', 'docker_image']
