"""
CinderVolumeLog - file ``/var/log/cinder/volume.log``
=====================================================

This is a standard log parser based on the LogFileOutput class.

Sample input::

    2015-06-19 07:31:41.020 7947 DEBUG cinder.openstack.common.periodic_task [-] Running periodic task VolumeManager._publish_service_capabilities run_periodic_tasks /usr/lib/python2.7/site-packages/cinder/openstack/common/periodic_task.py:178
    2015-06-19 07:31:42.220 7947 DEBUG cinder.manager [-] Notifying Schedulers of capabilities ... _publish_service_capabilities /usr/lib/python2.7/site-packages/cinder/manager.py:128
    2015-06-19 07:31:47.319 7947 DEBUG cinder.openstack.common.periodic_task [-] Running periodic task VolumeManager._report_driver_status run_periodic_tasks /usr/lib/python2.7/site-packages/cinder/openstack/common/periodic_task.py:178
    2015-06-19 07:32:53.612 7947 INFO cinder.volume.manager [-] Updating volume status
    2015-06-19 07:33:15.976 7947 DEBUG cinder.volume.drivers.nfs [-] shares loaded: {u'10.80.233.141:/opsfs1nvv4': None, u'hfdnnascl01-vs1n1.healthehostt.com:/hfdnnascl01vol1/cdrvol1hdnqt0': None} _load_shares_config /usr/lib/python2.7/site-packages/cinder/volume/drivers/nfs.py:327

Examples:

    >>> logs = shared[CinderVolumeLog]
    >>> 'Updating volume status' in logs
    True
    >>> logs.get('cinder.openstack.common.periodic_task')
    ['2015-06-19 07:31:41.020 7947 DEBUG cinder.openstack.common.periodic_task [-] Running periodic task VolumeManager._publish_service_capabilities run_periodic_tasks /usr/lib/python2.7/site-packages/cinder/openstack/common/periodic_task.py:178',
     '2015-06-19 07:31:47.319 7947 DEBUG cinder.openstack.common.periodic_task [-] Running periodic task VolumeManager._report_driver_status run_periodic_tasks /usr/lib/python2.7/site-packages/cinder/openstack/common/periodic_task.py:178']
    >>> from datetime import datetime
    >>> logs.get_after(datetime(2015, 6, 19, 7, 32, 0))
    ['2015-06-19 07:32:53.612 7947 INFO cinder.volume.manager [-] Updating volume status',
     '2015-06-19 07:33:15.976 7947 DEBUG cinder.volume.drivers.nfs [-] shares loaded: {u'10.80.233.141:/opsfs1nvv4': None, u'hfdnnascl01-vs1n1.healthehostt.com:/hfdnnascl01vol1/cdrvol1hdnqt0': None} _load_shares_config /usr/lib/python2.7/site-packages/cinder/volume/drivers/nfs.py:327']
"""

from .. import LogFileOutput, parser


@parser('cinder_volume.log')
class CinderVolumeLog(LogFileOutput):
    """
    Provide access to Cinder volume logs using the LogFileOutput parser class.
    """
    pass
