from insights.mappers.cinder_log import CinderVolumeLog
from insights.tests import context_wrap

import unittest

CINDER_LOG = """
2015-06-19 07:31:41.020 7947 DEBUG cinder.openstack.common.periodic_task [-] Running periodic task VolumeManager._publish_service_capabilities run_periodic_tasks /usr/lib/python2.7/site-packages/cinder/openstack/common/periodic_task.py:178
2015-06-19 07:31:41.022 7947 DEBUG cinder.manager [-] Notifying Schedulers of capabilities ... _publish_service_capabilities /usr/lib/python2.7/site-packages/cinder/manager.py:128
2015-06-19 07:31:41.025 7947 DEBUG cinder.openstack.common.periodic_task [-] Running periodic task VolumeManager._report_driver_status run_periodic_tasks /usr/lib/python2.7/site-packages/cinder/openstack/common/periodic_task.py:178
2015-06-19 07:31:41.026 7947 INFO cinder.volume.manager [-] Updating volume status
2015-06-19 07:31:41.026 7947 DEBUG cinder.volume.drivers.nfs [-] shares loaded: {u'10.80.233.141:/opsfs1nvv4': None, u'hfdnnascl01-vs1n1.healthehostt.com:/hfdnnascl01vol1/cdrvol1hdnqt0': None} _load_shares_config /usr/lib/python2.7/site-packages/cinder/volume/drivers/nfs.py:327
"""


class TestCinderLog(unittest.TestCase):
    def test_get_cinder_log(self):
        log = CinderVolumeLog(context_wrap(CINDER_LOG))
        self.assertEqual(len(log.lines), 5)
        self.assertEqual(log.get('cinder.volume.manager'), ['2015-06-19 07:31:41.026 7947 INFO cinder.volume.manager [-] Updating volume status'])
