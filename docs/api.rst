Input Data Formats
==================

Before any data reaches the rules framework, it obviously has to be generated.
There are currently several input data formats that can be processed by insights-core:

SoSReports
----------

A SoSReport_ is a command-line tool for Red Hat Enterprise Linux (and other
systems) to collect configuration and diagnostic information from the system.

.. _SoSReport: https://github.com/sos/sosreport

Insights Archives
-----------------

These archives have been designed from the ground up to fit the Insights
use case -- that is, to be automatically uploaded on a daily basis.
This means that the data contained in the archive is exactly what is
required to effectively process all currently-developed rules -- and
nothing more.

In addition, there are several features built in to the
insights-client_ package (which is the tool that creates Insights
archives) to better meet Red Hat customers' security and privacy concerns.

.. _insights-client: https://github.com/redhataccess/insights-client

Blacklists
    A list of files or commands to never upload.
Filters
    A set of grep-like strings used to filter files before adding it to
    the archive.
Dynamic Uploader Configuration
    The client will download a configuration file from Red Hat (by
    default) ever time it's executed that will list out every file to
    collect and command to run, including filters to apply to each file,
    specified by rule plugins.  The configuration is signed, which
    should be verified by the client before using it to collect data.

These features allow these archives to be processed quickly and more
securely in the Insights production environment.  On the other hand, the
reduced data set narrows the scope of uses to be Insights-specific.

Execution Model
===============

To build rules effectively, one should have a general idea of how data
is executed against each rule.  At a high level:

- Each unit of input data is mapped to a symbolic name
- Each parser that "subscribes" to that symbolic name is executed with
  the given content as part of a ``Context`` object.
- The outputs of all parsers are sorted by host
- For each host, every rule is invoked with the local context,
  populated by parsers from the same plugin, and the shared
  context, the combination of all shared parser outputs for this
  particular host.
- The outputs of all rules is returned, along with other various bits
  of metadata, to the client, depending on what invoked the rules
  framework.

Parsers
=======

A parser takes the raw content of a particular file or command output (from our
specs), parses it, and then provides a small API for plugins to query.  The
parsed data and computed facts available via the API are also serialized to be
used in downstream processes.

Choosing a Module
-----------------

Currently all shared parsers are defined in the package
``insights.parsers``.  From there, the parsers are separated into
modules based on the command or file that the parser consumes.  Commands or
files that are logically grouped together can go in the same module, e.g. the
``ethtool`` based commands and ``ps`` based commands.

Defining Parsers
----------------

There are a couple things that make a function a parser:

1. The function is decorated with the ``@parser`` decorator
2. The function takes one parameter, which is expected to be of type
   ``Context``.

Registration and Symbolic Names
-------------------------------

Parsers are registered with the framework by use of the ``@parser`` decorator.
This decorator will add the function object to the list of parsers associated
with the given symbolic name.  Without the decorator, the parser will
never be found by the framework.

Symbolic names represent all the possible file content types that can be
analyzed by parsers.  The rules framework uses the symbolic name mapping
defined in ``insights.specs.static`` to map a symbolic name to either a
command or absolute file path.  The same mapping is used to create the
``uploader.json`` file consumed by Insights clients to collect data from
customer systems.

.. autofunction:: insights.core.plugins.parser
   :noindex:

Parser Contexts
---------------

Each parser takes exactly one parameter, which is expected to be of type
``Context``.  All information available to a parser is found in the
``Context`` object.  Please refer to the `Context API documentation
</api_index.html#insights.core.context.Context>`_ for
more details.

Parser Outputs
--------------

Parsers can return any value, as long as it's serializable.

Parser developers are encouraged to wrap output data in a ``Parser``
class.  This makes plugin developers able to query for higher-level facts about
a particular file, while also exporting the higher level facts for use outside
of Insights plugins.

.. autoclass:: insights.core.Parser
   :members:
   :noindex:

Plugins (Rules)
==================

The purpose of "plugins" is to identify a particular problem in a given system
based on certain facts about that system.  Each plugin consists of a module
with:

- One ``@rule``-decorated function
- An ``ERROR_KEY`` member (recommended)
- A docstring for the module that includes
    - A summary of the plugin
    - A longer description of what the plugin identifies
    - A Trello/Jira link

.. autofunction:: insights.core.plugins.rule
   :noindex:

Rule Context
---------------

Each rule function must have only two parameters, named ``local`` and
``shared``.  The ``local`` parameter contains parser outputs from local (i.e.
legacy) parsers, and the ``shared`` parameter contains parser outputs from
shared parsers.  Since local parsers are considered deprecated, the ``local``
parameter will eventually be removed.

.. note::
   New plugins should avoid using the ``local`` context since it is deprecated.

The ``shared`` context is a dictionary where the keys are the function object
of the parser that produced the output.  This means that plugins must import
every parser that they intend to use, and they should list the function objects
in the ``requires`` keyword argument to the ``@rule`` decorator, if
applicable.  If the symbolic name for the given parser is a pattern file, then
the value of the parser's output will be a list, otherwise it will be whatever
the parser returns.  If the given parser returns a ``Parser`` instance,
plugins are are encouraged to use the higher-level functions defined on the
given ``Parser`` object to perform its business logic over functions
performed directly on the built-in data structures found in the
``Parser`` instance.

Rule Output
--------------

Rules can return two types of responses:  a rule "hit" or "action", or
system metadata.

To return a rule "hit", return the result of ``make_response``:

.. autofunction:: insights.core.plugins.make_response
   :noindex:

To return system metadata, return the result of ``make_metadata``:

.. autofunction:: insights.core.plugins.make_metadata
   :noindex:


Testing
=======

Since the plugin itself is a fairly simple set of python functions,
individual functions can be easily unit tested.  Unit tests are required
for all plugins and can be found in the ``rules/tests`` directory of the
source.  Unit tests are written using the usual x-unit based
``unittests`` module with some helpers from
`pytest framework <http://pytest.org/latest/>`_. ``pytest`` is the used
test runner.

To run all unit tests with pytest:

    py.test

Run a single single unit test one can:

    py.test path/test_plugin_name.py::TestCaseClass::test_method

To get test results with coverage report:

    py.test  --cov=plugin_package