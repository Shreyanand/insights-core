from falafel.mappers.fstab import fstab
from falafel.tests import context_wrap

FSTAB_TEST = """
UUID=9c286a1f-7f21-457a-8b30-4890b26966da swap                    swap    defaults        0 0
tmpfs                   /dev/shm                tmpfs   defaults,size=256m 0 0
""".strip()

class TestFstab():
    def test_fstab(self):
        fstab_info = fstab(context_wrap(FSTAB_TEST))
        assert ("swap" in fstab_info) == True

        assert fstab_info.parse_fstab() == [{"fs_spec": "UUID=9c286a1f-7f21-457a-8b30-4890b26966da", "fs_file": "swap", "fs_vfstype": "swap", "fs_mntops": "defaults", "fs_freq": "0", "fs_passno": "0"}, {"fs_spec": "tmpfs", "fs_file": "/dev/shm", "fs_vfstype": "tmpfs", "fs_mntops": "defaults,size=256m", "fs_freq": "0", "fs_passno": "0"}]
