"""
LsEtc - command ``ls -lanR /etc``
=================================

The ``ls -lanR /etc`` command provides information for the listing of the
``/etc`` directory.

Sample input is shown in the Examples. See ``FileListing`` class for
additional information.

Examples:
    >>> LS_ETC = '''
    ... /etc/sysconfig:
    ... total 96
    ... drwxr-xr-x.  7 0 0 4096 Jul  6 23:41 .
    ... drwxr-xr-x. 77 0 0 8192 Jul 13 03:55 ..
    ... drwxr-xr-x.  2 0 0   41 Jul  6 23:32 cbq
    ... drwxr-xr-x.  2 0 0    6 Sep 16  2015 console
    ... -rw-------.  1 0 0 1390 Mar  4  2014 ebtables-config
    ... -rw-r--r--.  1 0 0   72 Sep 15  2015 firewalld
    ... lrwxrwxrwx.  1 0 0   17 Jul  6 23:32 grub -> /etc/default/grub
    ...
    ... /etc/rc.d/rc3.d:
    ... total 4
    ... drwxr-xr-x.  2 0 0   58 Jul  6 23:32 .
    ... drwxr-xr-x. 10 0 0 4096 Sep 16  2015 ..
    ... lrwxrwxrwx.  1 0 0   20 Jul  6 23:32 K50netconsole -> ../init.d/netconsole
    ... lrwxrwxrwx.  1 0 0   17 Jul  6 23:32 S10network -> ../init.d/network
    ... lrwxrwxrwx.  1 0 0   15 Jul  6 23:32 S97rhnsd -> ../init.d/rhnsd
    ... '''
    >>> ls_etc = LsEtc(context_wrap(LS_ETC))
    >>> ls_etc
    <insights.parsers.ls_etc.LsEtc object at 0x7f287406a1d0>
    >>> "sysconfig" in ls_etc
    False
    >>> "/etc/sysconfig" in ls_etc
    True
    >>> ls_etc.files_of("/etc/sysconfig")
    ['ebtables-config', 'firewalld', 'grub']
    >>> ls_etc.dirs_of("/etc/sysconfig")
    ['.', '..', 'cbq', 'console']
    >>> ls_etc.specials_of("/etc/sysconfig")
    []
    >>> ls_etc.total_of("/etc/sysconfig")
    96
    >>> ls_etc.listing_of("/etc/sysconfig").keys()
    ['console', 'grub', '..', 'firewalld', '.', 'cbq', 'ebtables-config']
    >>> ls_etc.listing_of("/etc/sysconfig")['console'].keys()
    ['group', 'name', 'links', 'perms', 'raw_entry', 'owner', 'date', 'type', 'size']
    >>> ls_etc.listing_of("/etc/sysconfig")['console']['type']
    'd'
    >>> ls_etc.listing_of("/etc/sysconfig")['console']['perms']
    'rwxr-xr-x.'
    >>> ls_etc.dir_contains("/etc/sysconfig", "console")
    True
    >>> ls_etc.dir_entry("/etc/sysconfig", "console")
    {'group': '0', 'name': 'console', 'links': 2, 'perms': 'rwxr-xr-x.',
     'raw_entry': 'drwxr-xr-x.  2 0 0    6 Sep 16  2015 console', 'owner': '0',
     'date': 'Sep 16  2015', 'type': 'd', 'size': 6}
    >>> ls_etc.dir_entry("/etc/sysconfig", "grub")['type']
    'l'
    >>> ls_etc.dir_entry("/etc/sysconfig", "grub")['link']
    '/etc/default/grub'
"""
from .. import parser
from .. import FileListing
from insights.specs import Specs


@parser(Specs.ls_etc)
class LsEtc(FileListing):
    """Parses output of ``ls -lanR /etc`` command."""
    pass
