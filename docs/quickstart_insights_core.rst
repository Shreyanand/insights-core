###############################
Quickstart Insights Development
###############################

.. contents:: Table of Contents
    :depth: 6

Insights-core is the framework upon which Red Hat Insights rules are built and
delivered.  The basic purpose is to apply "rules" to a set of files collected
from a system at a given point in time.

Insights-core rule "plugins" are written in Python.  The rules follow a
"MapReduce" approach, dividing the logic between "mapping" and
"reducing" methods.  This is a convenient approach where a rule's logic
takes place in two steps.  First, there is a "gathering of facts" (the
map phase) followed by logic being applied to the facts (the reduce
phase).

*************
Prerequisites
*************

All Plugin code is written in Python and all Insights libraries
and framework code necessary for development and execution are
stored in Git repositories.  Before you begin make sure you have
the following installed:

* Python 2.7
* Git
* Python Virtualenv
* Python PIP

Further requirements can be found in the
`README.md <https://github.com/RedHatInsights/insights-core/blob/master/README.md>`_
file associated with the insights-core project.

**********************
Rule Development Setup
**********************

In order to develop rules to run in Red Hat Insights you'll need Insights
Core (http://github.com/RedHatInsights/insights-core) as well as your own rules code.

Clone the project::

    git clone git@github.com:RedHatInsights/insights-core.git

Or, alternatively, using HTTPS::

    git clone https://github.com/RedHatInsights/insights-core.git

Initialize a virtualenv::

    cd insights-core
    virtualenv .

Install the project and its dependencies::

    bin/pip install -e .

Install a rule repository::

    bin/pip install -e path/to/rule/repo

For a more detailed description of how to develop your own rules see the Tutorial
section :ref:`tutorial-rule-development`.

*****************
Contributor Setup
*****************

If you wish to contribute to the insights-core project you'll need to create a fork in github.

1. Clone your fork::

    git clone git@github.com:your-user/insights-core.git

2. Reference the original project as "upstream"::

    git remote add upstream git@github.com:RedHatInsights/insights-core.git

At this point, you would synchronize your fork with the upstream project
using the following commands::

    git pull upstream master
    git push origin master

You will need to initialize the project per the
`readme.md <https://github.com/RedHatInsights/insights-core/blob/master/README.md>`_
file.  For more detailed information about writing parsers and combiners see the
tutorial sections :ref:`tutorial-parser-development` and
:ref:`tutorial-combiner-development`.

***********************
Contributor Submissions
***********************

Contributors should submit changes to the code via github "Pull
Requests."  One would normally start a new contribution with a branch
from the current master branch of the upstream project.

1. Synchronize your fork as described in the Contributor Setup above

2. Make a branch on the fork.  Use a branch name that would be
   meaningful as it will be part of a default commit message when the
   topic branch is merged into the upstream project::

    git checkout -b your-topic

3. Make contributions on the topic branch.  Push them to your fork
   (creating a remote topic branch on your fork)::

    git push

4. If you need to make updates after pushing, it is useful to rebase
   with master.  This will change history, so you will need to force the
   push (this is fine on a topic branch when other developers are not
   working from the remote branch.) ::

    git checkout master
    git pull --rebase upstream master
    git push
    git checkout your-topic
    git rebase master
    git push

    You may have to use the `git push --force` command depending upon
    the changes you have made since the initial commit of your pull
    request.

5. Generally, keep the number of commits on the topic branch small.
   Usually a single commit, perhaps a few in some cases.  Use the
   ``amend`` and ``rebase -i`` git commands to manage the commit history
   of the topic branch.  Again, such manipulations change history and
   require a ``--force`` push.

6. When ready, use the github UI to submit a pull request.

7. Repeat steps 4 and 5 as necessary.  Note that a forced push to the
   topic branch will work as expected.  The pull request will be
   updated with the current view of the topic-branch.

*****************
Style Conventions
*****************


Code Style
==========

Code style mostly follows `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_.
The style followed is essentially encoded in the
`flake8 <http://flake8.pycqa.org/en/latest/>`_ configuration file in the
repo's root directory.  The current configuration specifies the
following rules as exceptions

- E501: Line too long
- E126: Continuation line over-indented for hanging indent
- E127: Continuation line over-indented for visual indent
- E128: Continuation line under-indented for visual indent

In some cases, a particular bit of code may require formatting that
violates flake8 rules.  In such cases, one can, for example, annotate
the line with ``# noqa`` to ignore all errors/warnings or ``# noqa: E501,W291``
to ignore only **E501** errors and **W291** warnings.
Override flake8 checking sparingly.

Code that does not pass the project's current flake8 tests
will not be accepted.


Commit Message Style
====================

Commit messages are an important description of changes taking place in
the code base. So, they should be effective at providing useful
descriptions of the changes for someone browsing the git log.

Generally, they should follow the usual
`git conventions <http://chris.beams.io/posts/git-commit/>`_.

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line
4. Do not end the subject line with a period
5. Use the imperative mood in the subject line
6. Wrap the body at 72 characters
7. Use the body to explain the *what* and *why* vs. *how*


Documentation
=============

Code should generally be clear enough to self-document the *how* of the
implementation.  Of course, when a bit of code isn't clear, comments may
be needed.

Documentation in the form of pydoc should be considered to document
usage of code as necessary.  In particular, code used by rule developers
should be carefully documented.  They should be able to use generated
documentation to understand, for example, the data models exposed by
parser classes.  For further details, see the
:ref:`documentation_guidelines` included in this guide.

****************
Review Checklist
****************

The following checklist is used when reviewing pull requests


General (all submissions)
=========================

- Commit messages are useful and properly formatted
- Unit tests validate the code submission
- One commit, or at most only a handful.  More than five commits should
  be heavily questioned


Parsers
=======

- Parser is properly documented per the :ref:`documentation_guidelines`
  and should include

   - Example input 
   - The resulting data structure represented by the parser
   - Parser usage is clear to a user with some knowledge of the domain
     without needing to examine the code itself
   - Meaning and usage of an "empty" (falsy data object) is clear

- Unit tests cover both positive and negative cases and utilizes
  reasonable examples of input data. Test data should be usable in the
  generation in archives used for integration testing and product
  demonstrations.

- Parsers do not expose a ``defaultdict`` or any other data structure that
  would mutate as a side effect of accessing the object.
