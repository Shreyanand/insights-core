"""
foreman_log - Files /var/log/foreman...
=======================================


Module for parsing the log files in foreman-debug archive

Note:
    Please refer to its super-class ``LogFileOutput``

"""

from .. import LogFileOutput, parser


@parser('foreman_proxy.log')
class ProxyLog(LogFileOutput):
    """Class for parsing ``foreman-proxy/proxy.log`` file."""
    time_format = '%d/%b/%Y %H:%M:%S'


@parser('foreman_satellite.log')
class SatelliteLog(LogFileOutput):
    """Class for parsing ``foreman-installer/satellite.log`` file."""
    pass


@parser('foreman_production.log')
class ProductionLog(LogFileOutput):
    """Class for parsing ``foreman/production.log`` file."""
    pass


@parser('candlepin.log')
class CandlepinLog(LogFileOutput):
    """Class for parsing ``candlepin/candlepin.log`` file."""
    pass
