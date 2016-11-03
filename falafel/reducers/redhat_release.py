"""
Red Hat Release
===============

Shared reducer for Red Hat Release information. It uses the results of
the ``Uname`` mapper and the ``rht_release`` mapper to determine the release
major and minor version.  ``Uname`` is the preferred source of data. The Red
Hat Release is in obtained from the system in the form major.minor.  For
example for a Red Hat Enterprise Linux 7.2 system, the release would be
major = 7 and minor = 2.  The returned values are in integer format.Re

Examples:
    >>> rh_release = shared[redhat_release]
    >>> rh_release.major
    7
    >>> rh_release.minor
    2
    >>> rh_release
    Release(major=7, minor=2)

"""

from collections import namedtuple
from falafel.core.plugins import reducer
from falafel.mappers.redhat_release import RedhatRelease as rht_release
from falafel.mappers.uname import Uname

Release = namedtuple("Release", field_names=["major", "minor"])
"""namedtuple: Type for storing the release information."""


@reducer(requires=[[rht_release, Uname]], shared=True)
def redhat_release(local, shared):
    """Check uname and redhat-release for rhel major/minor version.

    Prefer uname to redhat-release.

    Returns:
        release (Release): A named tuple with `major` and `minor` version
        components.

    Raises:
        Exeption: If the version can't be determined even though a Uname
            or RedhatRelease was provided.
    """

    un = shared.get(Uname)
    if un and un.release_tuple[0] != -1:
        return Release(*un.release_tuple)

    rh_release = shared.get(rht_release)
    if rh_release:
        return Release(rh_release.major, rh_release.minor)

    raise Exception("Unabled to determine release.")
