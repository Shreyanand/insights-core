"""
ls /dev - Command
=================

The ``ls -lanR /dev`` command provides information for the listing of the
``/dev`` directory.

Sample input is shown in the Examples. See ``FileListing`` class for
additional information.

Examples:
    >>> LS_DEV = '''
    ... /dev:
    ... total 3
    ... brw-rw----.  1 0  6 253,   0 Aug  4 16:56 dm-0
    ... brw-rw----.  1 0  6 253,   1 Aug  4 16:56 dm-1
    ... brw-rw----.  1 0  6 253,  10 Aug  4 16:56 dm-10
    ... crw-rw-rw-.  1 0  5   5,   2 Aug  5  2016 ptmx
    ... drwxr-xr-x.  2 0  0        0 Aug  4 16:56 pts
    ... lrwxrwxrwx.  1 0  0       25 Oct 25 14:48 initctl -> /run/systemd/initctl/fifo
    ...
    ... /dev/rhel:
    ... total 0
    ... drwxr-xr-x.  2 0 0  100 Jul 25 10:00 .
    ... drwxr-xr-x. 23 0 0 3720 Jul 25 12:43 ..
    ... lrwxrwxrwx.  1 0 0    7 Jul 25 10:00 home -> ../dm-2
    ... lrwxrwxrwx.  1 0 0    7 Jul 25 10:00 root -> ../dm-0
    ... lrwxrwxrwx.  1 0 0    7 Jul 25 10:00 swap -> ../dm-1
    ...'''
    >>> ls_dev = LsDev(context_wrap(LS_DEV))
    >>> ls_dev
    <falafel.mappers.ls_dev.LsDev object at 0x7f287406a1d0>
    >>> "/dev/rhel" in ls_dev
    True
    >>> ls_dev.files_of("/dev/rhel")
    ['home', 'root', 'swap']
    >>> ls_dev.dirs_of("/dev/rhel")
    ['.', '..']
    >>> ls_dev.specials_of("/dev/rhel")
    []
    >>> ls_dev.listing_of("/dev/rhel").keys()
    ['home', 'root', 'swap', '..', '.']
    >>> ls_dev.dir_entry("/dev/rhel", "home")
    {'group': '0', 'name': 'home', 'links': 1, 'perms': 'rwxrwxrwx.',
    'raw_entry': 'lrwxrwxrwx.  1 0 0    7 Jul 25 10:00 home -> ../dm-2', 'owner': '0',
    'link': '../dm-2', 'date': 'Jul 25 10:00', 'type': 'l', 'size': 7}
    >>> ls_dev.listing_of('/dev/rhel')['.']['type'] == 'd'
    True
    >>> ls_dev.listing_of('/dev/rhel')['home']['link']
    '../dm-2'
"""
from .. import mapper, FileListing


@mapper("ls_dev")
class LsDev(FileListing):
    """Parses output of ``ls -lanR /dev`` command."""
    pass


@mapper("ls_dev")
def parse_ls_dev(context):
    """
        We still reserve this method here just for compatibility as the refactoring will cause existing plugins in CEEPH fail.
        Don't use this method anymore. It will be deprecated later.
    """
    dicts = dict()
    files = list()
    dir = ""
    for line in context.content:
        if not line:
            dicts[dir] = files
            files = list()
        elif line.strip().endswith(":"):
            dir = line.split(":")[0]
        elif line.startswith('b'):
            files.append(line.split()[-1])
        elif line.startswith('l'):
            files.append(line.split()[-3])
    dicts[dir] = files
    return dicts
