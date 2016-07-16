from falafel.mappers import blkid
from falafel.tests import context_wrap

BLKID_INFO = """
/dev/sda1: UUID="3676157d-f2f5-465c-a4c3-3c2a52c8d3f4" TYPE="xfs"
/dev/sda2: UUID="UVTk76-UWOc-vk7s-galL-dxIP-4UXO-0jG4MH" TYPE="LVM2_member"
/dev/mapper/rhel_hp--dl160g8--3-root: UUID="11124c1d-990b-4277-9f74-c5a34eb2cd04" TYPE="xfs"
/dev/mapper/rhel_hp--dl160g8--3-swap: UUID="c7c45f2d-1d1b-4cf0-9d51-e2b0046682f8" TYPE="swap"
/dev/mapper/rhel_hp--dl160g8--3-home: UUID="c7116820-f2de-4aee-8ea6-0b23c6491598" TYPE="xfs"
/dev/mapper/rhel_hp--dl160g8--3-lv_test: UUID="d403bcbd-0eea-4bff-95b9-2237740f5c8b" TYPE="ext4"
/dev/cciss/c0d1p3: LABEL="/u02" UUID="004d0ca3-373f-4d44-a085-c19c47da8b5e" TYPE="ext3"
/dev/loop0: LABEL="Satellite-5.6.0 x86_64 Disc 0" TYPE="iso9660"
""".strip()


class TestBLKID():
    def test_get_blkid_info(self):
        blkid_dict = blkid.get_blkid_info(context_wrap(BLKID_INFO))
        assert len(blkid_dict) == 8
        assert blkid_dict.get('/dev/sda1') == {
            'UUID': '3676157d-f2f5-465c-a4c3-3c2a52c8d3f4',
            'TYPE': 'xfs'
        }
        assert blkid_dict.get('/dev/cciss/c0d1p3') == {
            'LABEL': '/u02',
            'UUID': '004d0ca3-373f-4d44-a085-c19c47da8b5e',
            'TYPE': 'ext3'
        }
        assert blkid_dict['/dev/sda2'].get('UUID') == 'UVTk76-UWOc-vk7s-galL-dxIP-4UXO-0jG4MH'
        assert blkid_dict['/dev/sda2'].get('TYPE') == 'LVM2_member'
        assert blkid_dict['/dev/mapper/rhel_hp--dl160g8--3-lv_test'].get('TYPE') == 'ext4'
        assert blkid_dict['/dev/cciss/c0d1p3'].get('LABEL') == '/u02'
        assert blkid_dict['/dev/loop0'].get('LABEL') == 'Satellite-5.6.0 x86_64 Disc 0'
