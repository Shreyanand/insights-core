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
    def get_after(self, timestamp, lines=None):
        """
        Get a list of lines after the given time stamp.

        Parameters:
            timestamp(datetime.datetime): log lines after this time are
                returned.
            lines(list): the list of log lines to search (e.g. from a get).
                If not supplied, all available lines are searched.

        Returns:
            (list): The list of log lines with time stamps after the given
            date and time.
        """
        return super(ProxyLog, self).get_after(timestamp, lines, '%d/%b/%Y %H:%M:%S')


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
