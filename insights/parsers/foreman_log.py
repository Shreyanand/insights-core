"""
foreman_log - Files /var/log/foreman...
=======================================


Module for parsing the log files in foreman-debug archive

Note:
    Please refer to its super-class ``LogFileOutput``

"""

from .. import LogFileOutput, parser
from insights.specs import candlepin_error_log
from insights.specs import candlepin_log
from insights.specs import foreman_production_log
from insights.specs import foreman_proxy_log
from insights.specs import foreman_satellite_log


@parser(foreman_proxy_log)
class ProxyLog(LogFileOutput):
    """Class for parsing ``foreman-proxy/proxy.log`` file."""
    time_format = {
        'standard': '%d/%b/%Y:%H:%M:%S',  # 31/May/2016:09:57:34
        'error': '%Y-%m-%dT%H:%M:%S.%f'  # 2016-05-31T09:57:35.884636
    }


@parser(foreman_satellite_log)
class SatelliteLog(LogFileOutput):
    """Class for parsing ``foreman-installer/satellite.log`` file."""
    pass


@parser(foreman_production_log)
class ProductionLog(LogFileOutput):
    """Class for parsing ``foreman/production.log`` file."""
    pass


@parser(candlepin_log)
class CandlepinLog(LogFileOutput):
    """Class for parsing ``candlepin/candlepin.log`` file."""
    pass


@parser(candlepin_error_log)
class CandlepinErrorLog(LogFileOutput):
    """
    Class for parsing ``candlepin/error.log`` file.

    Sample log contents::

        2016-09-07 13:56:49,001 [=, org=] WARN  org.apache.qpid.transport.network.security.ssl.SSLUtil - Exception received while trying to verify hostname
        2016-09-07 14:07:33,735 [=, org=] WARN  org.apache.qpid.transport.network.security.ssl.SSLUtil - Exception received while trying to verify hostname
        2016-09-07 14:09:55,173 [=, org=] WARN  org.apache.qpid.transport.network.security.ssl.SSLUtil - Exception received while trying to verify hostname
        2016-09-07 15:20:33,796 [=, org=] WARN  org.apache.qpid.transport.network.security.ssl.SSLUtil - Exception received while trying to verify hostname
        2016-09-07 15:27:34,367 [=, org=] WARN  org.apache.qpid.transport.network.security.ssl.SSLUtil - Exception received while trying to verify hostname
        2016-09-07 16:49:24,650 [=, org=] WARN  org.apache.qpid.transport.network.security.ssl.SSLUtil - Exception received while trying to verify hostname
        2016-09-07 18:07:53,688 [req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28, org=org_ray] ERROR org.candlepin.sync.Importer - Conflicts occurred during import that were
        2016-09-07 18:07:53,690 [req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28, org=org_ray] ERROR org.candlepin.sync.Importer - [DISTRIBUTOR_CONFLICT]
        2016-09-07 18:07:53,711 [req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28, org=org_ray] ERROR org.candlepin.resource.OwnerResource - Recording import failure
        org.candlepin.sync.ImportConflictException: Owner has already imported from another subscription management application.

    Examples:
        >>> candlepin_log = shared[Candlepin_Error_Log]
        >>> candlepin_log.get('req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28')
        ['2016-09-07 18:07:53,688 [req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28, org=org_ray] ERROR org.candlepin.sync.Importer - Conflicts occurred during import that were
        not overridden:', '2016-09-07 18:07:53,690 [req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28, org=org_ray] ERROR org.candlepin.sync.Importer - [DISTRIBUTOR_CONFLICT]',
        '2016-09-07 18: 07:53,711 [req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28, org=org_ray] ERROR org.candlepin.resource.OwnerResource - Recording import failure
        org.candlepin.sync.ImportConflit Exception: Owner has already imported from another subscription management application.']

        >>> candlepin_log.get_after(datetime(2016, 9, 7, 16, 0, 0)
        ['2016-09-07 16:49:24,650 [=, org=] WARN  org.apache.qpid.transport.network.security.ssl.SSLUtil - Exception received while trying to verify hostname',
        '2016-09-07 18:7:53,688 [req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28, org=org_ray] ERROR org.candlepin.sync.Importer - Conflicts occurred during import that
        were not overridden:', '2016-09-07 18:07:53,690 [req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28, org=org_ray] ERROR org.candlepin.sync.Importer - [DISTRIBUTOR_CONFLICT]',
        '2016-09-07 18:07:53,711 [req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28, org=org_ray] ERROR org.candlepin.resource.OwnerResource - Recording import failure
        org.candlepin.sync.ImportConflictException: Owner has already imported from another subscription management application.']

    """
    pass
