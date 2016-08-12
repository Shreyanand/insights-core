from falafel.mappers import lvm
from falafel.tests import context_wrap

VGS_INFO = """
LVM2_VG_FMT='lvm2'|LVM2_VG_UUID='YCpusB-LEly-THGL-YXhC-t3q6-mUQV-wyFZrx'|LVM2_VG_NAME='rhel'|LVM2_VG_ATTR='wz--n-'|LVM2_VG_PERMISSIONS='writeable'|LVM2_VG_EXTENDABLE='extendable'|LVM2_VG_EXPORTED=''|LVM2_VG_PARTIAL=''|LVM2_VG_ALLOCATION_POLICY='normal'|LVM2_VG_CLUSTERED=''|LVM2_VG_SIZE='476.45g'|LVM2_VG_FREE='4.00m'|LVM2_VG_SYSID=''|LVM2_VG_SYSTEMID=''|LVM2_VG_LOCKTYPE=''|LVM2_VG_LOCKARGS=''|LVM2_VG_EXTENT_SIZE='4.00m'|LVM2_VG_EXTENT_COUNT='121971'|LVM2_VG_FREE_COUNT='1'|LVM2_MAX_LV='0'|LVM2_MAX_PV='0'|LVM2_PV_COUNT='1'|LVM2_LV_COUNT='3'|LVM2_SNAP_COUNT='0'|LVM2_VG_SEQNO='4'|LVM2_VG_TAGS=''|LVM2_VG_PROFILE=''|LVM2_VG_MDA_COUNT='1'|LVM2_VG_MDA_USED_COUNT='1'|LVM2_VG_MDA_FREE='0 '|LVM2_VG_MDA_SIZE='1020.00k'|LVM2_VG_MDA_COPIES='unmanaged'
LVM2_VG_FMT='lvm2'|LVM2_VG_UUID='123456-LEly-THGL-YXhC-t3q6-mUQV-123456'|LVM2_VG_NAME='fedora'|LVM2_VG_ATTR='wz--n-'|LVM2_VG_PERMISSIONS='writeable'|LVM2_VG_EXTENDABLE='extendable'|LVM2_VG_EXPORTED=''|LVM2_VG_PARTIAL=''|LVM2_VG_ALLOCATION_POLICY='normal'|LVM2_VG_CLUSTERED=''|LVM2_VG_SIZE='476.45g'|LVM2_VG_FREE='4.00m'|LVM2_VG_SYSID=''|LVM2_VG_SYSTEMID=''|LVM2_VG_LOCKTYPE=''|LVM2_VG_LOCKARGS=''|LVM2_VG_EXTENT_SIZE='4.00m'|LVM2_VG_EXTENT_COUNT='121971'|LVM2_VG_FREE_COUNT='1'|LVM2_MAX_LV='0'|LVM2_MAX_PV='0'|LVM2_PV_COUNT='1'|LVM2_LV_COUNT='3'|LVM2_SNAP_COUNT='0'|LVM2_VG_SEQNO='4'|LVM2_VG_TAGS=''|LVM2_VG_PROFILE=''|LVM2_VG_MDA_COUNT='1'|LVM2_VG_MDA_USED_COUNT='1'|LVM2_VG_MDA_FREE='0 '|LVM2_VG_MDA_SIZE='1020.00k'|LVM2_VG_MDA_COPIES='unmanaged'

""".strip()


def test_vgs():
    vgs_records = lvm.vgs(context_wrap(VGS_INFO))
    assert len(vgs_records) == 2
    assert vgs_records[1] == {
        'LVM2_VG_FMT': 'lvm2',
        'LVM2_VG_UUID': '123456-LEly-THGL-YXhC-t3q6-mUQV-123456',
        'LVM2_VG_NAME': 'fedora',
        'LVM2_VG_ATTR': 'wz--n-',
        'LVM2_VG_PERMISSIONS': 'writeable',
        'LVM2_VG_EXTENDABLE': 'extendable',
        'LVM2_VG_EXPORTED': '',
        'LVM2_VG_PARTIAL': '',
        'LVM2_VG_ALLOCATION_POLICY': 'normal',
        'LVM2_VG_CLUSTERED': '',
        'LVM2_VG_SIZE': '476.45g',
        'LVM2_VG_FREE': '4.00m',
        'LVM2_VG_SYSID': '',
        'LVM2_VG_SYSTEMID': '',
        'LVM2_VG_LOCKTYPE': '',
        'LVM2_VG_LOCKARGS': '',
        'LVM2_VG_EXTENT_SIZE': '4.00m',
        'LVM2_VG_EXTENT_COUNT': '121971',
        'LVM2_VG_FREE_COUNT': '1',
        'LVM2_MAX_LV': '0',
        'LVM2_MAX_PV': '0',
        'LVM2_PV_COUNT': '1',
        'LVM2_LV_COUNT': '3',
        'LVM2_SNAP_COUNT': '0',
        'LVM2_VG_SEQNO': '4',
        'LVM2_VG_TAGS': '',
        'LVM2_VG_PROFILE': '',
        'LVM2_VG_MDA_COUNT': '1',
        'LVM2_VG_MDA_USED_COUNT': '1',
        'LVM2_VG_MDA_FREE': '0 ',
        'LVM2_VG_MDA_SIZE': '1020.00k',
        'LVM2_VG_MDA_COPIES': 'unmanaged'
    }
    assert vgs_records[0].get("LVM2_VG_FMT") == "lvm2"
    assert vgs_records[0].get("LVM2_VG_UUID") == "YCpusB-LEly-THGL-YXhC-t3q6-mUQV-wyFZrx"
