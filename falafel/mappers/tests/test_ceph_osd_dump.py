from falafel.mappers.ceph_osd_dump import CephOsdDump
from falafel.tests import context_wrap


CEPH_OSD_DUMP_INFO = """
{
    "epoch": 210,
    "fsid": "2734f9b5-2013-48c1-8e96-d31423444717",
    "created": "2016-11-12 16:08:46.307206",
    "modified": "2017-03-07 08:55:53.301911",
    "flags": "sortbitwise",
    "cluster_snapshot": "",
    "pool_max": 12,
    "max_osd": 8,
    "pools": [
        {
            "pool": 0,
            "pool_name": "rbd",
            "flags": 1,
            "flags_names": "hashpspool",
            "type": 1,
            "size": 3,
            "min_size": 2,
            "crush_ruleset": 0,
            "object_hash": 2,
            "pg_num": 256
        }
    ]
}
""".strip()


def test_ceph_osd_dump():

    result = CephOsdDump(context_wrap(CEPH_OSD_DUMP_INFO)).data

    assert result == {
                'pool_max': 12, 'max_osd': 8,
                'created': '2016-11-12 16:08:46.307206',
                'modified': '2017-03-07 08:55:53.301911',
                'epoch': 210, 'flags': u'sortbitwise',
                'cluster_snapshot': '',
                'fsid': '2734f9b5-2013-48c1-8e96-d31423444717',
                'pools': [
                            {
                                'pool_name': 'rbd', 'flags_names': 'hashpspool',
                                'min_size': 2, 'object_hash': 2, 'flags': 1,
                                'pg_num': 256, 'crush_ruleset': 0, 'type': 1,
                                'pool': 0, 'size': 3
                            }
                          ]
            }

    assert result['pools'][0]['min_size'] == 2
