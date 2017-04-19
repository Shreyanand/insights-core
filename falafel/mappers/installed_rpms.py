"""
installed RPMs - Command ``rpm -qa``
====================================
The ``InstalledRpms`` class parses the output of the ``rpm -qa`` command.  Each line
is parsed and stored in an ``InstalledRpm`` object.  The ``rpm -qa`` command may
output data in different formats and each format can be handled by the parsing
routines of this class. The basic format of command is the package and is shown
in the Examples.

Sample input data::

    a52dec-0.7.4-18.el7.nux.x86_64  Tue 14 Jul 2015 09:25:38 AEST   1398536494
    aalib-libs-1.4.0-0.22.rc5.el7.x86_64    Tue 14 Jul 2015 09:25:40 AEST   1390535634
    abrt-2.1.11-35.el7.x86_64       Wed 09 Nov 2016 14:52:01 AEDT   1446193355
    ...
    kernel-3.10.0-230.el7synaptics.1186112.1186106.2.x86_64 Wed 20 May 2015 11:24:00 AEST   1425955944
    kernel-3.10.0-267.el7.x86_64    Sat 24 Oct 2015 09:56:17 AEDT   1434466402
    kernel-3.10.0-327.36.3.el7.x86_64       Wed 09 Nov 2016 14:53:25 AEDT   1476954923
    kernel-headers-3.10.0-327.36.3.el7.x86_64       Wed 09 Nov 2016 14:20:59 AEDT   1476954923
    kernel-tools-3.10.0-327.36.3.el7.x86_64 Wed 09 Nov 2016 15:09:42 AEDT   1476954923
    kernel-tools-libs-3.10.0-327.36.3.el7.x86_64    Wed 09 Nov 2016 14:52:13 AEDT   1476954923
    kexec-tools-2.0.7-38.el7_2.1.x86_64     Wed 09 Nov 2016 14:48:21 AEDT   1452845178
    ...
    zlib-1.2.7-15.el7.x86_64        Wed 09 Nov 2016 14:21:19 AEDT   1431443476
    zsh-5.0.2-14.el7_2.2.x86_64     Wed 09 Nov 2016 15:13:19 AEDT   1464185248


Examples:
    >>> from falafel.mappers.installed_rpms import InstalledRpms
    >>> from falafel.tests import context_wrap
    >>> content = '''
    ... openjpeg-libs-1.3-9.el6_3.x86_64
    ... openldap-2.4.23-31.el6.x86_64
    ... openobex-1.4-7.el6.x86_64
    ... openssh-server-5.3p1-104.el6.x86_64
    ... openssh-askpass-5.3p1-84.1.el6.x86_64
    ... openssl-1.0.0-27.el6.x86_64
    ... '''
    >>> shared = {InstalledRpms: InstalledRpms(context_wrap(content))}
    >>> rpms = shared[InstalledRpms]
    >>> 'openjpeg-libs' in rpms
    True
    >>> rpms.corrupt
    False
    >>> rpms.get_max('openjpeg-libs')
    0:openjpeg-libs-1.3-9.el6_3
    >>> type(rpms.get_max('openjpeg-libs'))
    <class 'falafel.mappers.installed_rpms.InstalledRpm'>
    >>> rpms.get_min('openjpeg-libs')
    0:openjpeg-libs-1.3-9.el6_3
    >>> rpm = rpms.get_max('openssh-server')
    >>> rpm
    0:openssh-server-5.3p1-104.el6
    >>> type(rpm)
    <class 'falafel.mappers.installed_rpms.InstalledRpm'>
    >>> rpm.package
    'openssh-server-5.3p1-104.el6'
    >>> rpm.nvr
    'openssh-server-5.3p1-104.el6'
    >>> rpm.source
    >>> rpm.name
    'openssh-server'
    >>> rpm.version
    '5.3p1'
    >>> rpm.release
    '104.el6'
    >>> rpm.arch
    'x86_64'
    >>> rpm.epoch
    '0'
    >>> from falafel.mappers.installed_rpms import InstalledRpm
    >>> rpm2 = InstalledRpm.from_package('openssh-server-6.0-100.el6.x86_64')
    >>> rpm == rpm2
    False
    >>> rpm > rpm2
    False
    >>> rpm < rpm2
    True
"""
import json
from collections import defaultdict
from distutils.version import LooseVersion as LV

from ..util import rsplit
from .. import Mapper, mapper, get_active_lines

# This list of architectures is taken from PDC (Product Definition Center):
# https://pdc.fedoraproject.org/rest_api/v1/arches/
KNOWN_ARCHITECTURES = [
    # Common architectures
    'x86_64',
    'i386',
    'i486',
    'i586',
    'i686',
    'src',
    'ia64',
    'ppc',
    'ppc64',
    's390',
    's390x',
    'amd64',
    '(none)',
    'noarch',
    # Less common
    'alpha',
    'alphaev4',
    'alphaev45',
    'alphaev5',
    'alphaev56',
    'alphaev6',
    'alphaev67',
    'alphaev68',
    'alphaev7',
    'alphapca56',
    'arm64',
    'armv5tejl',
    'armv5tel',
    'armv6l',
    'armv7hl',
    'armv7hnl',
    'armv7l',
    'athlon',
    'armhfp',
    'geode',
    'ia32e',
    'nosrc',
    'ppc64iseries',
    'ppc64le',
    'ppc64p7',
    'ppc64pseries',
    'sh3',
    'sh4',
    'sh4a',
    'sparc',
    'sparc64',
    'sparc64v',
    'sparcv8',
    'sparcv9',
    'sparcv9v',
    'aarch64',
]
"""list: List of recognized architectures.

This list is taken from the PDC (Product Definition Center) available
here https://pdc.fedoraproject.org/rest_api/v1/arches/.
"""


@mapper('installed-rpms')
class InstalledRpms(Mapper):
    """
    A mapper for working with data containing a list of installed RPM files on the system and
    related information.
    """
    def __init__(self, *args, **kwargs):
        self.errors = []
        """list: List of input lines that indicate an error acquiring the data on the client."""
        self.unparsed = []
        """list: List of input lines that raised an exception during parsing."""
        self.packages = defaultdict(list)
        """dict (InstalledRpm): Dictionary of RPMs keyed by package name."""

        super(InstalledRpms, self).__init__(*args, **kwargs)

    def parse_content(self, content):
        for line in get_active_lines(content, comment_char='COMMAND>'):
            if line.startswith('error:') or line.startswith('warning:'):
                self.errors.append(line)
            else:
                try:
                    # Try to parse from JSON input
                    rpm = InstalledRpm.from_json(line)
                    self.packages[rpm.name].append(rpm)
                except Exception:
                    # If that fails, try to parse from line input
                    if line.strip():
                        try:
                            rpm = InstalledRpm.from_line(line)
                            self.packages[rpm.name].append(rpm)
                        except Exception:
                            # Both ways failed
                            self.unparsed.append(line)
        # Don't want defaultdict's behavior after parsing is complete
        self.packages = dict(self.packages)

    def __contains__(self, package_name):
        """
        Checks if package name is in list of installed RPMs.

        Args:
            package_name (str): RPM package name such as 'bash'

        Returns:
            bool: True if package name is in list of installed packages, otherwise False
        """
        return package_name in self.packages

    @property
    def corrupt(self):
        """bool: True if RPM database is corrupted, else False."""
        return any('rpmdbNextIterator' in s for s in self.errors)

    def get_max(self, package_name):
        """
        Returns the highest version of the installed package with the given name.

        Args:
            package_name (str): Installed RPM package name such as 'bash'

        Returns:
            InstalledRpm: Installed RPM with highest version
        """
        if package_name not in self.packages:
            return None
        else:
            return max(self.packages[package_name])

    def get_min(self, package_name):
        """
        Returns the lowest version of the installed package with the given name.

        Args:
            package_name (str): Installed RPM package name such as 'bash'.

        Returns:
            InstalledRpm: Installed RPM with lowest version
        """
        if package_name not in self.packages:
            return None
        else:
            return min(self.packages[package_name])

    @property
    def is_hypervisor(self):
        """bool: True if ".el[6|7]ev" exists in "vdsm".release, else False."""
        rpm = self.get_max("vdsm")
        return (True if rpm and rpm.release.endswith((".el6ev", ".el7ev")) else
                False)


class InstalledRpm(object):
    """
    Class for holding information about one installed RPM.

    This class is usually created from dictionary with following structure::

         {
            'name': 'package name',
            'version': 'package version',
            'release': 'package release,
            'arch': 'package architecture'
          }

    It may also contain supplementary information from SOS report or epoch
    information from JSON.

    Factory methods are provided such as ``from_package`` to create an object from a
    short package string::

        kernel-devel-3.10.0-327.36.1.el7.x86_64

    ``from_json`` to create an object from JSON::

       {"name": "kernel-devel",
        "version": "3.10.0",
        "release": "327.36.1.el7",
        "arch": "x86_64"}

    and ``from_line`` to create an object from a long package string:

        .. code:: python

            ('kernel-devel-3.10.0-327.36.1.el7.x86_64'
             '                                '
             'Wed May 18 14:16:21 2016' '\t'
             '1410968065' '\t'
             'Red Hat, Inc.' '\t'
             'hs20-bc2-4.build.redhat.com' '\t'
             '8902150305004...b3576ff37da7e12e2285358267495ac48a437d4eefb3213' '\t'
             'RSA/8, Mon Aug 16 11:14:17 2010, Key ID 199e2f91fd431d51')
    """
    SOSREPORT_KEYS = [
        'installtime', 'buildtime', 'vendor', 'buildserver', 'pgpsig', 'pgpsig-short'
    ]
    """list: List of keys for SOS Report RPM information."""

    def __init__(self, data):
        self.name = None
        """str: RPM package name."""
        self.version = None
        """str: RPM package version."""
        self.release = None
        """str: RPM package release."""
        self.arch = None
        """str: RPM package architecture."""

        for k, v in data.iteritems():
            setattr(self, k, v)
        if 'epoch' not in data:
            self.epoch = '0'

        """Below is only for version comparison"""
        def _start_of_distribution(rest_split):
            """
            The start of distribution field: from the right, the last non-digit part
            - bash-4.2.39-3.el7_2.2
              distribution: el7_2.2
            - kernel-rt-debug-3.10.0-327.rt56.204.el7
              distribution: el7
            """
            nondigit_flag = False
            for i, r in enumerate(reversed(rest_split)):
                if not r.isdigit():
                    nondigit_flag = True
                elif nondigit_flag and r.isdigit():
                    return len(rest_split) - i

        self._release_sep = self.release
        self._distribution = None
        rl_split = self._release_sep.split('.') if self._release_sep else None
        idx = _start_of_distribution(rl_split) if rl_split else None
        if idx:
            self._release_sep = '.'.join(rl_split[:idx])
            self._distribution = '.'.join(rl_split[idx:])

    @classmethod
    def from_package(cls, package_string):
        """
        The object of this class is usually created from dictionary. Alternatively it can be
        created from package string.

        Args:
            package_string (str): package string in the following format (shown as Python string)::

                'kernel-devel-3.10.0-327.36.1.el7.x86_64'
        """
        return cls(cls._parse_package(package_string))

    @classmethod
    def from_json(cls, json_line):
        """
        The object of this class is usually created from dictionary. Alternatively it can be
        created from JSON line.

        Args:
            json_line (str): JSON string in the following format (shown as Python string)::

                '{"name": "kernel-devel", "version": "3.10.0", "release": "327.36.1.el7", "arch": "x86_64"}'
        """
        return cls(json.loads(json_line))

    @classmethod
    def from_line(cls, line):
        """
        The object of this class is usually created from dictionary. Alternatively it can be
        created from package line.

        Args:
            line (str): package line in the following format (shown as Python string):

                .. code-block:: python

                    ('kernel-devel-3.10.0-327.36.1.el7.x86_64'
                     '                                '
                     'Wed May 18 14:16:21 2016' '\t'
                     '1410968065' '\t'
                     'Red Hat, Inc.' '\t'
                     'hs20-bc2-4.build.redhat.com' '\t'
                     '8902150305004...b3576ff37da7e12e2285358267495ac48a437d4eefb3213' '\t'
                     'RSA/8, Mon Aug 16 11:14:17 2010, Key ID 199e2f91fd431d51')

        """
        return cls(cls._parse_line(line))

    @staticmethod
    def _arch_sep(package_string):
        """
        Helper method for finding if arch separator is '.' or '-'

        Args:
            package_string (str): dash separated package string such as 'bash-4.2.39-3.el7'.

        Returns:
            str: arch separator
        """
        return '.' if package_string.rfind('.') > package_string.rfind('-') else '-'

    @classmethod
    def _parse_package(cls, package_string):
        """
        Helper method for parsing package string.

        Args:
            package_string (str): dash separated package string such as 'bash-4.2.39-3.el7'

        Returns:
            dict: dictionary containing 'name', 'version', 'release' and 'arch' keys
        """
        pkg, arch = rsplit(package_string, cls._arch_sep(package_string))
        if arch not in KNOWN_ARCHITECTURES:
            pkg, arch = (package_string, None)
        pkg, release = rsplit(pkg, '-')
        name, version = rsplit(pkg, '-')
        return {
            'name': name,
            'version': version,
            'release': release,
            'arch': arch
        }

    @classmethod
    def _parse_line(cls, line):
        """
        Helper method for parsing package line with or without SOS report information.

        Args:
            line (str): package line with or without SOS report information

        Returns:
            dict: dictionary containing 'name', 'version', 'release' and 'arch' keys plus
                  additionally 'installtime', 'buildtime', 'vendor', 'buildserver', 'pgpsig',
                  'pgpsig-short' if these are present.
        """
        try:
            pkg, rest = line.split(None, 1)
        except ValueError:
            rpm = cls._parse_package(line.strip())
            return rpm
        rpm = cls._parse_package(pkg)
        rest = rest.split('\t')
        for i, value in enumerate(rest):
            rpm[cls.SOSREPORT_KEYS[i]] = value
        return rpm

    @property
    def package(self):
        """str: Package `name-version-release` string."""
        return '{}-{}-{}'.format(self.name,
                                 self.version,
                                 self.release)

    @property
    def nvr(self):
        """str: Package `name-version-release` string."""
        return self.package

    @property
    def nvra(self):
        """str: Package `name-version-release.arch` string."""
        return ".".join([self.package, self.arch])

    @property
    def source(self):
        """InstalledRpm: Returns source RPM of this RPM object."""
        if hasattr(self, 'srpm'):
            rpm = self.from_package(self.srpm)
            # Source RPMs don't have epoch for some reason
            rpm.epoch = self.epoch
            return rpm

    def __getitem__(self, item):
        """
        Allows to use `rpm["element"]` instead of `rpm.element`. Dot notation should be preferred,
        however it is especially useful for values containing dash, such as "pgpsig-short".
        """
        return getattr(self, item)

    def __str__(self):
        return '{}:{}'.format(self.epoch, self.package)

    def __unicode__(self):
        return unicode(str(self))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, InstalledRpm):
            return False

        if self.name != other.name:
            raise ValueError('Cannot compare packages with differing names {} != {}'
                             .format(self.name, other.name))
        if (not self._distribution) != (not other._distribution):
            raise ValueError('Cannot compare packages that one has distribution while the other does not {} != {}'
                             .format(self.package, other.package))

        eq_ret = (type(self) == type(other) and
                  LV(self.epoch) == LV(other.epoch) and
                  LV(self.version) == LV(other.version) and
                  LV(self.release) == LV(other.release))

        if self._distribution:
            return eq_ret and LV(self._distribution) == LV(other._distribution)
        else:
            return eq_ret

    def __lt__(self, other):
        if not isinstance(other, InstalledRpm):
            return False

        if self == other:
            return False

        self_ep, other_ep = LV(self.epoch), LV(other.epoch)
        if self_ep != other_ep:
            return self_ep < other_ep

        self_v, other_v = LV(self.version), LV(other.version)
        if self_v != other_v:
            return self_v < other_v

        self_rl, other_rl = LV(self._release_sep), LV(other._release_sep)
        if self_rl != other_rl:
            return self_rl < other_rl

        if self._distribution:
            return LV(self._distribution) < LV(other._distribution)

        return False

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return isinstance(other, InstalledRpm) and other.__lt__(self)

    def __ge__(self, other):
        return isinstance(other, InstalledRpm) and not self.__lt__(other)

    def __le__(self, other):
        return isinstance(other, InstalledRpm) and not other.__lt__(self)


@mapper('installed-rpms')
class OracleAsmRpms(Mapper):
    """Parse installed rpms for oracleasm RPM.

    This class parses the installed rpms and saves all versions of the
    oracleasm RPM that is installed. The Oracle Asm RPM has two version
    numbers embedded, like this `oracleasm-2.6.18-164.el5-2.0.5-1.el5.x86_64`.

    This mapper filters out the `oracleasmlib` and `oracleasm-support` rpms.

    Examples:
        >>> shared[OracleAsmRpms].rpms_installed
        ['oracleasm-2.6.18-164.el5-2.0.5-1.el5.x86_64']
    """
    def parse_content(self, content):
        self._data = []
        for line in get_active_lines(content, comment_char='COMMAND>'):
            if line.startswith('oracleasm-'):
                if 'support' not in line:
                    self._data.append(line)

    @property
    def rpms_installed(self):
        """list (str): Returns a list of the installed oracleasm rpms."""
        return self._data
