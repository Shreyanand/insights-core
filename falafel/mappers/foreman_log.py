"""
foreman_log - Files /var/log/foreman...
=======================================


Module for parsing the log files in foreman-debug archive

Note:
    Please refer to its super-class ``LogFileOutput``

"""

from .. import LogFileOutput, mapper


@mapper('foreman_proxy.log')
class ProxyLog(LogFileOutput):
    """Class for parsing ``foreman-proxy/proxy.log`` file."""
    pass


@mapper('foreman_satellite.log')
class SatelliteLog(LogFileOutput):
    """Class for parsing ``foreman-installer/satellite.log`` file."""
    pass


@mapper('foreman_production.log')
class ProductionLog(LogFileOutput):
    """Class for parsing ``foreman/production.log`` file."""
    pass


@mapper('candlepin.log')
class CandlepinLog(LogFileOutput):
    """Class for parsing ``candlepin/candlepin.log`` file."""
    pass
