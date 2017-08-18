"""
RHNConf - file ``/etc/rhn/rhn.conf``
====================================

"""

from insights import Parser, parser, LegacyItemAccess
from insights.parsers import get_active_lines


@parser('rhn.conf')
class RHNConf(LegacyItemAccess, Parser):
    """
    Class to parse the configuration file ``rhn.conf``.

    The special feature of ``rhn.conf`` is that values can span multiple
    lines with each intermediate line ending with a comma.

    This parser uses the :class:`insights.core.LegacyItemAccess` mix-in to provide
    access to its data directly.

    Attributes:
        data (dict): A dictionary of values keyed by the configuration
            item.  Values spanning multiple lines are compacted together.
            Values that include a comma are turned into lists.


    Sample ``rhn.conf`` input::

        # Corporate gateway (hostname:PORT):
        server.satellite.http_proxy = corporate_gateway.example.com:8080
        server.satellite.http_proxy_username =
        server.satellite.http_proxy_password =
        traceback_mail = test@pobox.com, test@redhat.com

        web.default_taskmaster_tasks = RHN::Task::SessionCleanup,
                                       RHN::Task::ErrataQueue,
                                       RHN::Task::ErrataEngine,
                                       RHN::Task::DailySummary,
                                       RHN::Task::SummaryPopulation,
                                       RHN::Task::RHNProc,
                                       RHN::Task::PackageCleanup

    Examples:
        >>> conf = shared[RHNConf]
        >>> conf.data['server.satellite.http_proxy']  # Long form access
        'corporate_gateway.example.com:8080'
        >>> conf['server.satellite.http_proxy']  # Short form access
        'corporate_gateway.example.com:8080'
        >>> conf['traceback_mail']  # split into a list
        ['test@pobox.com', 'test@redhat.com']
        >>> conf['web.default_taskmaster_tasks'][3]  # Values can span multiple lines
        'RHN::Task::DailySummary'
    """

    def parse_content(self, content):
        rhn = {}
        is_multi = False
        multi_lines_key = None
        for line in get_active_lines(content):
            if line.endswith(','):
                line = line[:-1]
                is_multi = True
            else:
                is_multi = False

            if '=' in line:
                k, v = [i.strip() for i in line.split('=', 1)]
                multi_lines_key = k if is_multi else None
                rhn[k] = [i.strip() for i in v.split(',')] if ',' in v else [v] if is_multi else v
            elif multi_lines_key:
                rhn[multi_lines_key].extend([i.strip() for i in line.split(',')] if ',' in line else [line])
        self.data = rhn
