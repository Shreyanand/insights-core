import pytest
from insights.parsers import kdump
from insights.tests import context_wrap

KDUMP_WITH_NORMAL_COMMENTS = """
# this is a comment

ssh kdumpuser@10.209.136.62
path /kdump/raw
core_collector makedumpfile -c --message-level 1 -d 31
""".strip()

KDUMP_WITH_INLINE_COMMENTS = """
nfs4 10.209.136.62:/kdumps
path /kdump/raw #some path stuff
core_collector makedumpfile -c --message-level 1 -d 31
""".strip()

KDUMP_WITH_EQUAL = """
nfs 10.209.136.62:/kdumps
path /kdump/raw #some path stuff
core_collector makedumpfile -c --message-level 1 -d 31
some_var "blah=3"
options bonding mode=active-backup miimon=100
""".strip()

KDUMP_WITH_BLACKLIST = """
path /var/crash
core_collector makedumpfile -c --message-level 1 -d 24
default shell
blacklist vxfs
blacklist vxportal
blacklist vxted
blacklist vxcafs
blacklist fdd
ignore_me
"""

KDUMP_WITH_NET = """
net user@raw.server.com
raw /dev/sda5
""".strip()

KDUMP_MATCH_1 = """
net user@raw.server.com
raw /dev/sda5
""".strip()


def test_with_normal_comments():
    context = context_wrap(KDUMP_WITH_NORMAL_COMMENTS)
    kd = kdump.KDumpConf(context)
    expected = "# this is a comment"
    assert expected == kd.comments[0]
    # Also test is_* properties
    assert not kd.is_nfs()
    assert kd.is_ssh()
    # Not a local disk then.
    assert not kd.using_local_disk


def test_with_inline_comments():
    context = context_wrap(KDUMP_WITH_INLINE_COMMENTS)
    kd = kdump.KDumpConf(context)
    expected = "path /kdump/raw #some path stuff"
    assert expected == kd.inline_comments[0]
    assert "/kdump/raw" == kd["path"]
    # Also test is_* properties
    assert kd.is_nfs()
    assert not kd.is_ssh()
    # Not a local disk then.
    assert not kd.using_local_disk


def test_with_equal():
    context = context_wrap(KDUMP_WITH_EQUAL)
    kd = kdump.KDumpConf(context)
    expected = '"blah=3"'
    assert expected == kd['some_var']
    assert 'options' in kd.data
    assert isinstance(kd.data['options'], dict)
    assert 'bonding' in kd.data['options']
    assert 'mode=active-backup miimon=100' == kd.data['options']['bonding']
    # Alternate accessor for options:
    assert kd.options('bonding') == 'mode=active-backup miimon=100'
    # Also test is_* properties
    assert kd.is_nfs()
    assert not kd.is_ssh()
    # Not a local disk then.
    assert not kd.using_local_disk


def test_get_hostname():
    context = context_wrap(KDUMP_WITH_EQUAL)
    kd = kdump.KDumpConf(context)
    assert '10.209.136.62' == kd.hostname

    context = context_wrap(KDUMP_MATCH_1)
    kd = kdump.KDumpConf(context)
    assert 'raw.server.com' == kd.hostname


def test_get_ip():
    context = context_wrap(KDUMP_WITH_EQUAL)
    kd = kdump.KDumpConf(context)
    assert '10.209.136.62' == kd.ip

    context = context_wrap(KDUMP_MATCH_1)
    kd = kdump.KDumpConf(context)
    assert kd.ip is None


def test_blacklist_repeated():
    context = context_wrap(KDUMP_WITH_BLACKLIST)
    kd = kdump.KDumpConf(context)
    assert 'blacklist' in kd.data
    assert kd.data['blacklist'] == ['vxfs', 'vxportal', 'vxted', 'vxcafs', 'fdd']
    # Also test is_* properties
    assert not kd.is_nfs()
    assert not kd.is_ssh()
    assert kd.using_local_disk


def test_net_and_raw():
    context = context_wrap(KDUMP_WITH_NET)
    kd = kdump.KDumpConf(context)
    assert 'net' in kd.data
    assert 'raw' in kd.data
    assert kd.using_local_disk
    with pytest.raises(TypeError):
        assert kd[3]


KEXEC_CRASH_SIZE_1 = "134217728"
KEXEC_CRASH_SIZE_2 = "0"
KEXEC_CRASH_SIZE_BAD = ""


def test_kexec_crash_size():
    kcs = kdump.KexecCrashSize(context_wrap(KEXEC_CRASH_SIZE_1))
    assert kcs.size == 134217728
    kcs = kdump.KexecCrashSize(context_wrap(KEXEC_CRASH_SIZE_2))
    assert kcs.size == 0
    kcs = kdump.KexecCrashSize(context_wrap(KEXEC_CRASH_SIZE_BAD))
    assert kcs.size == 0


KDUMP_CRASH_NOT_LOADED = '0'
KDUMP_CRASH_LOADED = '1'
KDUMP_CRASH_LOADED_BAD = ''


def test_loaded():
    ctx = context_wrap(KDUMP_CRASH_LOADED, path='/sys/kernel/kexec_crash_loaded')
    assert kdump.KexecCrashLoaded(ctx).is_loaded


def test_not_loaded():
    ctx = context_wrap(KDUMP_CRASH_NOT_LOADED, path='/sys/kernel/kexec_crash_loaded')
    assert not kdump.KexecCrashLoaded(ctx).is_loaded


def test_loaded_bad():
    ctx = context_wrap(KDUMP_CRASH_LOADED_BAD, path='/sys/kernel/kexec_crash_loaded')
    assert not kdump.KexecCrashLoaded(ctx).is_loaded
