import unittest

from falafel.mappers import mdstat
from falafel.tests import context_wrap

MDSTAT_TEST_1 = """
Personalities : [raid1] [raid6] [raid5] [raid4]
md_d0 : active raid5 sde1[0] sdf1[4] sdb1[5] sdd1[2] cciss/c0d0p1[6] sdc1[1]
      1250241792 blocks super 1.2 level 5, 64k chunk, algorithm 2 [5/5] [UUUUUU]
      bitmap: 0/10 pages [0KB], 16384KB chunk

unused devices: <none>
""".strip()

MDSTAT_RESULT_1 = {"personalities": ["raid1", "raid6", "raid5", "raid4"],
        "components": [{"device_name": "md_d0", "active": True, "auto_read_only": False, "raid": "raid5", "component_name": "sde1", "device_flag": '', "role": 0, "up": True},
            {"device_name": "md_d0", "active": True, "auto_read_only": False, "raid": "raid5", "component_name": "sdf1", "device_flag": '', "role": 4, "up": True},
            {"device_name": "md_d0", "active": True, "auto_read_only": False, "raid": "raid5", "component_name": "sdb1", "device_flag": '', "role": 5, "up": True},
            {"device_name": "md_d0", "active": True, "auto_read_only": False, "raid": "raid5", "component_name": "sdd1", "device_flag": '', "role": 2, "up": True},
            {"device_name": "md_d0", "active": True, "auto_read_only": False, "raid": "raid5", "component_name": "cciss/c0d0p1", "device_flag": '', "role": 6, "up": True},
            {"device_name": "md_d0", "active": True, "auto_read_only": False, "raid": "raid5", "component_name": "sdc1", "device_flag": '', "role": 1, "up": True}]
                   }

MDSTAT_TEST_2 = """
Personalities : [raid1] [raid6] [raid5] [raid4]
md1 : active raid1 sdb2[1] sda2[0]
      136448 blocks [2/2] [UU]

md2 : active raid1 sdb3[1] sda3[0]
      129596288 blocks [2/2] [U_]

md0 : active raid1 sdb1[1](F) sda1[0]
      16787776 blocks [2/2] [_U]

unused devices: <none>
""".strip()

MDSTAT_RESULT_2 = {"personalities": ["raid1", "raid6", "raid5", "raid4"],
        "components": [{"device_name": "md1", "active": True, "auto_read_only": False, "raid": "raid1", "component_name": "sdb2", "device_flag": '', "role": 1, "up": True},
            {"device_name": "md1", "active": True, "auto_read_only": False, "raid": "raid1", "component_name": "sda2", "device_flag": '', "role": 0, "up": True},
            {"device_name": "md2", "active": True, "auto_read_only": False, "raid": "raid1", "component_name": "sdb3", "device_flag": '', "role": 1, "up": True},
            {"device_name": "md2", "active": True, "auto_read_only": False, "raid": "raid1", "component_name": "sda3", "device_flag": '', "role": 0, "up": False},
            {"device_name": "md0", "active": True, "auto_read_only": False, "raid": "raid1", "component_name": "sdb1", "device_flag": 'F', "role": 1, "up": False},
            {"device_name": "md0", "active": True, "auto_read_only": False, "raid": "raid1", "component_name": "sda1", "device_flag": '', "role": 0, "up": True}]
                   }

MDSTAT_TEST_3 = """
Personalities : [linear] [raid0] [raid1]
unused devices: <none>
""".strip()

MDSTAT_RESULT_3 = {"personalities": ["linear", "raid0", "raid1"], "components": []}

MDSTAT_TEST_4 = """
Personalities : [linear] [raid0] [raid1]
md0 : inactive sdb[1](S) sda[0](S)
      6306 blocks super external:imsm<Paste>

unused devices: <none>
""".strip()

MDSTAT_RESULT_4 = {"personalities": ["linear", "raid0", "raid1"], "components": [
    {'device_flag': 'S', 'raid': None, 'device_name': 'md0', 'role': 1, 'active': False, 'auto_read_only': False, 'component_name': 'sdb'},
    {'device_flag': 'S', 'raid': None, 'device_name': 'md0', 'role': 0, 'active': False, 'auto_read_only': False, 'component_name': 'sda'}
]}

PERSONALITIES_TEST = "Personalities : [linear] [raid0] [raid1] [raid5] [raid4] [raid6]\n"

PERSONALITIES_FAIL = [
    "Some stupid line.",
    "Personalities [raid1]",
    "Personalities : [raid1] some trash"
]

MD_TEST_1 = "md0 : active raid6 sdf1[0] sde1[1] sdd1[2](F) sdc1[3] sdb1[4](F) sda1[5] hdb1[6]"
MD_RESULT_1 = [
        {"device_name": "md0", "active": True, "auto_read_only": False, "raid": "raid6", "component_name": "sdf1", "role": 0, "device_flag": ''},
        {"device_name": "md0", "active": True, "auto_read_only": False, "raid": "raid6", "component_name": "sde1", "role": 1, "device_flag": ''},
        {"device_name": "md0", "active": True, "auto_read_only": False, "raid": "raid6", "component_name": "sdd1", "role": 2, "device_flag": 'F'},
        {"device_name": "md0", "active": True, "auto_read_only": False, "raid": "raid6", "component_name": "sdc1", "role": 3, "device_flag": ''},
        {"device_name": "md0", "active": True, "auto_read_only": False, "raid": "raid6", "component_name": "sdb1", "role": 4, "device_flag": 'F'},
        {"device_name": "md0", "active": True, "auto_read_only": False, "raid": "raid6", "component_name": "sda1", "role": 5, "device_flag": ''},
        {"device_name": "md0", "active": True, "auto_read_only": False, "raid": "raid6", "component_name": "hdb1", "role": 6, "device_flag": ''}
]

MD_TEST_2 = "md0 : active (auto-read-only) raid6 sdf1[0] sde1[1] sdd1[2](S)"
MD_RESULT_2 = [
        {"device_name": "md0", "active": True, "auto_read_only": True, "raid": "raid6", "component_name": "sdf1", "role": 0, "device_flag": ''},
        {"device_name": "md0", "active": True, "auto_read_only": True, "raid": "raid6", "component_name": "sde1", "role": 1, "device_flag": ''},
        {"device_name": "md0", "active": True, "auto_read_only": True, "raid": "raid6", "component_name": "sdd1", "role": 2, "device_flag": 'S'}
]

MD_FAIL = [
    "what? : active raid5 sdh1[6] sdg1[4] sdf1[3] sde1[2] sdd1[1] sdc1[0]",
    "md124  active raid5 sdh1[6] sdg1[4] sdf1[3] sde1[2] sdd1[1] sdc1[0]",
    "md124 : raid5 sdh1[6] sdg1[4] sdf1[3] sde1[2] sdd1[1] sdc1[0]",
    "md124 : junk raid5 sdh1[6] sdg1[4] sdf1[3] sde1[2] sdd1[1] sdc1[0]",
    "md124 : active raid5 sdh16 sdg1[4] sdf1[3] sde1[2] sdd1[1] sdc1[0]",
    "md124 : active raid5 sdh1[6] sdg1[4]junk sdf1[3] sde1[2] sdd1[1] sdc1[0]"
    "md124 : active raid5 sdh1[6] sdg1[4]junk sdf1[3] sde1[2] sdd1[1] sdc1[0]"
]

UPSTRING_TEST_1 = "488383936 blocks [6/4] [_UUU_U]"
UPSTRING_TEST_2 = "1318680576 blocks level 5, 1024k chunk, algorithm 2 [10/10] [UUUUUUUUUU]"
UPSTRING_TEST_3 = "[==>..................]  recovery = 12.6% (37043392/292945152) finish=127.5min speed=33440K/sec"


class TestMdstat(unittest.TestCase):
    def test_parse_personalities(self):
        result = mdstat.parse_personalities(PERSONALITIES_TEST)
        self.assertEquals(["linear", "raid0", "raid1", "raid5", "raid4", "raid6"], result)

        for line in PERSONALITIES_FAIL:
            with self.assertRaises(AssertionError):
                mdstat.parse_personalities(line)

    def test_parse_array_start(self):
        result = mdstat.parse_array_start(MD_TEST_1)
        self.assertEquals(MD_RESULT_1, result)

        result = mdstat.parse_array_start(MD_TEST_2)
        self.assertEquals(MD_RESULT_2, result)

        for md_line in MD_FAIL:
            with self.assertRaises(AssertionError):
                mdstat.parse_array_start(md_line)

    def test_parse_upstring(self):
        result = mdstat.parse_upstring(UPSTRING_TEST_1)
        self.assertEquals('_UUU_U', result)

        result = mdstat.parse_upstring(UPSTRING_TEST_2)
        self.assertEquals('UUUUUUUUUU', result)

        result = mdstat.parse_upstring(UPSTRING_TEST_3)
        self.assertEquals(None, result)

    def test_apply_upstring(self):
        test_dict = [{}, {}, {}, {}]
        mdstat.apply_upstring('U_U_', test_dict)
        self.assertTrue(test_dict[0]['up'])
        self.assertFalse(test_dict[1]['up'])
        self.assertTrue(test_dict[2]['up'])
        self.assertFalse(test_dict[3]['up'])

        with self.assertRaises(AssertionError):
            mdstat.apply_upstring('U?_U', test_dict)

        with self.assertRaises(AssertionError):
            mdstat.apply_upstring('U_U', test_dict)

    def test_parse_content(self):
        result = mdstat.Mdstat.parse_content(MDSTAT_TEST_1.splitlines())
        self.assertEqual(MDSTAT_RESULT_1, result)

        result = mdstat.Mdstat.parse_content(MDSTAT_TEST_2.splitlines())
        self.assertEqual(MDSTAT_RESULT_2, result)

        result = mdstat.Mdstat.parse_content(MDSTAT_TEST_3.splitlines())
        self.assertEqual(MDSTAT_RESULT_3, result)

        result = mdstat.Mdstat.parse_content(MDSTAT_TEST_4.splitlines())
        self.assertEqual(MDSTAT_RESULT_4, result)

    def test_mdstat_construction(self):
        mdstat_obj = mdstat.Mdstat.parse_context(context_wrap(MDSTAT_TEST_1))
        self.assertEqual(MDSTAT_RESULT_1, mdstat_obj.data)

        mdstat_obj = mdstat.Mdstat.parse_context(context_wrap(MDSTAT_TEST_3))
        self.assertEqual(MDSTAT_RESULT_3, mdstat_obj.data)
