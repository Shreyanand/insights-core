"""
Sysconfig - files in ``/etc/sysconfig/``
========================================

This is a collection of parsers that all deal with the system's configuration
files under the ``/etc/sysconfig/`` folder.  Parsers included in this module
are:

ChronydSysconfig - file ``/etc/sysconfig/chronyd``
--------------------------------------------------

DockerSysconfig - file ``/etc/sysconfig/docker``
------------------------------------------------

HttpdSysconfig - file ``/etc/sysconfig/httpd``
----------------------------------------------

IrqbalanceSysconfig - file ``/etc/sysconfig/irqbalance``
--------------------------------------------------------

KdumpSysconfig - file ``/etc/sysconfig/kdump``
----------------------------------------------

MongodSysconfig - file ``/etc/sysconfig/mongod``
------------------------------------------------

NtpdSysconfig - file ``/etc/sysconfig/ntpd``
--------------------------------------------

VirtWhoSysconfig - file ``/etc/sysconfig/virt-who``
---------------------------------------------------

"""

from .. import parser, SysconfigOptions
from insights.specs import Specs


@parser(Specs.sysconfig_chronyd)
class ChronydSysconfig(SysconfigOptions):
    """
    A parser for analyzing the ``chronyd`` service config file in the
    ``/etc/sysconfig`` directory.

    Sample Input::

      OPTIONS="-d"
      #HIDE="me"

    Examples:

        >>> service_opts = shared[ChronydSysconfig]
        >>> 'OPTIONS' in service_opts
        True
        >>> 'HIDE' in service_opts
        False
        >>> service_opts['OPTIONS']
        '-d'

    """
    pass


@parser(Specs.sysconfig_ntpd)
class NtpdSysconfig(SysconfigOptions):
    """
    A parser for analyzing the ``ntpd`` service config file in the
    ``/etc/sysconfig`` directory

    Sample Input::

      OPTIONS="-x -g"
      #HIDE="me"

    Examples:

        >>> service_opts = shared[NtpdSysconfig]
        >>> 'OPTIONS' in service_opts
        True
        >>> 'HIDE' in service_opts
        False
        >>> service_opts['OPTIONS']
        '-x -g'
    """
    pass


@parser(Specs.docker_sysconfig)
class DockerSysconfig(SysconfigOptions):
    """
    Class for parsing the ``/etc/sysconfig/docker`` file using the standard
    ``SysconfigOptions`` parser class.  The 'OPTIONS' variable is also provided
    in the ``options`` property as a convenience.

    Examples:

    >>> conf = shared[DockerSysconfig]
    >>> 'OPTIONS' in conf
    True
    >>> conf['OPTIONS']
    '--selinux-enabled'
    >>> conf.options
    '--selinux-enabled'
    >>> conf['DOCKER_CERT_PATH']
    '/etc/docker'
    """

    @property
    def options(self):
        """ Return the value of the 'OPTIONS' variable, or '' if not defined. """
        return self.data.get('OPTIONS', '')


@parser(Specs.sysconfig_httpd)
class HttpdSysconfig(SysconfigOptions):
    """
    A parser for analyzing the ``httpd`` service config file in the
    ``/etc/sysconfig`` directory.

    Sample Input::

        # The default processing model (MPM) is the process-based
        # 'prefork' model.  A thread-based model, 'worker', is also
        # available, but does not work with some modules (such as PHP).
        # The service must be stopped before changing this variable.
        #
        HTTPD=/usr/sbin/httpd.worker
        #
        # To pass additional options (for instance, -D definitions) to the
        # httpd binary at startup, set OPTIONS here.
        #
        OPTIONS=

    Examples:

        >>> httpd_syscfg = shared[HttpdSysconfig]
        >>> httpd_syscfg['HTTPD']
        '/usr/sbin/httpd.worker'
        >>> httpd_syscfg.get('OPTIONS')
        ''
        >>> 'NOOP' in httpd_syscfg
        False

    """
    pass


@parser(Specs.sysconfig_irqbalance)
class IrqbalanceSysconfig(SysconfigOptions):
    """
    A parser for analyzing the ``irqbalance`` service config file in the
    ``/etc/sysconfig`` directory.

    Sample Input::

        #IRQBALANCE_ONESHOT=yes
        #
        # IRQBALANCE_BANNED_CPUS
        # 64 bit bitmask which allows you to indicate which cpu's should
        # be skipped when reblancing irqs. Cpu numbers which have their
        # corresponding bits set to one in this mask will not have any
        # irq's assigned to them on rebalance
        #
        IRQBALANCE_BANNED_CPUS=f8

        IRQBALANCE_ARGS="-d"

    Examples:

        >>> irqb_syscfg = shared[IrqbalanceSysconfig]
        >>> irqb_syscfg['IRQBALANCE_BANNED_CPUS']
        'f8'
        >>> irqb_syscfg.get('IRQBALANCE_ARGS')  # quotes will be stripped
        '-d'
        >>> irqb_syscfg.get('IRQBALANCE_ONESHOT')
        None
        >>> 'ONESHOT' in irqb_syscfg
        False

    """
    pass


@parser(Specs.sysconfig_kdump)
class KdumpSysconfig(SysconfigOptions):
    """
    Read data from the ``/etc/sysconfig/kdump`` file.

    This sets the following properties for ease of access:

    * KDUMP_COMMANDLINE
    * KDUMP_COMMANDLINE_REMOVE
    * KDUMP_COMMANDLINE_APPEND
    * KDUMP_KERNELVER
    * KDUMP_IMG
    * KDUMP_IMG_EXT
    * KEXEC_ARGS

    These are set to the value of the named variable in the kdump sysconfig
    file, or '' if not found.
    """

    KDUMP_KEYS = [
        'KDUMP_COMMANDLINE',
        'KDUMP_COMMANDLINE_REMOVE',
        'KDUMP_COMMANDLINE_APPEND',
        'KDUMP_KERNELVER',
        'KDUMP_IMG',
        'KDUMP_IMG_EXT',
        'KEXEC_ARGS',
    ]

    def parse_content(self, content):
        super(KdumpSysconfig, self).parse_content(content)
        for key in self.KDUMP_KEYS:
            setattr(self, key, self.data.get(key, ''))


@parser(Specs.sysconfig_virt_who)
class VirtWhoSysconfig(SysconfigOptions):
    """
    A parser for analyzing the ``virt-who`` service configuration file in the
    ``/etc/sysconfig`` directory.

    Sample Input::

        # Register ESX machines using vCenter
        # VIRTWHO_ESX=0
        # Register guests using RHEV-M
        VIRTWHO_RHEVM=1

        # Options for RHEV-M mode
        VIRTWHO_RHEVM_OWNER=

        TEST_OPT="A TEST"

    Examples:
        >>> vwho_syscfg = shared[VirtWhoSysconfig]
        >>> vwho_syscfg['VIRTWHO_RHEVM']
        '1'
        >>> vwho_syscfg.get('VIRTWHO_RHEVM_OWNER')
        ''
        >>> vwho_syscfg.get('NO_SUCH_OPTION')
        None
        >>> 'NOSUCHOPTION' in vwho_syscfg
        False
        >>> vwho_syscfg.get('TEST_OPT')  # Quotes are stripped
        'A TEST'
    """
    pass


@parser(Specs.sysconfig_mongod)
class MongodSysconfig(SysconfigOptions):
    """
    A parser for analyzing the ``mongod`` service configuration file in
    the ``etc/sysconfig`` directory, contains 'etc/sysconfig/mongod' and
    '/etc/opt/rh/rh-mongodb26/sysconfig/mongod'.

    Sample Input::

        OPTIONS="--quiet -f /etc/mongod.conf"

    Examples:
        >>> mongod_syscfg = shared[MongodSysconfig]
        >>> mongod_syscfg.get('OPTIONS')
        '--quiet -f /etc/mongod.conf'
        >>> mongod_syscfg.get('NO_SUCH_OPTION')
        None
        >>> 'NOSUCHOPTION' in mongod_syscfg
        False
    """
    pass
