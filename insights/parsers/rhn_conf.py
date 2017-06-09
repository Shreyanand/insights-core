from .. import Parser, parser, get_active_lines, LegacyItemAccess


@parser('rhn.conf')
class RHNConf(LegacyItemAccess, Parser):
    """Class to parse the configuration file ``rhn.conf``
    Attributes:
        data (dict): A dict where
        - keys are the row header
        - values are the option after the "=".
          Note: For settings with multiple options, the value is a list.

    """

    def parse_content(self, content):
        """
        ---Sample---
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
        -----------
        """

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
