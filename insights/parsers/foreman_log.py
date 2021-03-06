"""
Foreman and Candlepin logs
==========================

Module for parsing the log files in foreman-debug archive

.. note::
    Please refer to its super-class :class:`insights.core.LogFileOutput` for
    usage information.

Parsers provided by this module:

CandlepinErrorLog - file ``sos_commands/foreman/foreman-debug/var/log/candlepin/error.log``
-------------------------------------------------------------------------------------------

CandlepinLog - file ``/var/log/candlepin/candlepin.log``
--------------------------------------------------------

ProductionLog - file ``/var/log/foreman/production.log``
--------------------------------------------------------

ProxyLog - file ``/var/log/foreman-proxy/proxy.log``
----------------------------------------------------

SatelliteLog - file ``/var/log/foreman-installer/satellite.log``
----------------------------------------------------------------

"""

from .. import LogFileOutput, parser
from insights.specs import Specs


@parser(Specs.foreman_proxy_log)
class ProxyLog(LogFileOutput):
    """Class for parsing ``foreman-proxy/proxy.log`` file."""
    time_format = {
        'standard': '%d/%b/%Y:%H:%M:%S',  # 31/May/2016:09:57:34
        'error': '%Y-%m-%dT%H:%M:%S.%f'  # 2016-05-31T09:57:35.884636
    }


@parser(Specs.foreman_satellite_log)
class SatelliteLog(LogFileOutput):
    """Class for parsing ``foreman-installer/satellite.log`` file."""
    pass


@parser(Specs.foreman_production_log)
class ProductionLog(LogFileOutput):
    """Class for parsing ``foreman/production.log`` file."""
    pass


@parser(Specs.candlepin_log)
class CandlepinLog(LogFileOutput):
    """Class for parsing ``candlepin/candlepin.log`` file."""
    pass


@parser(Specs.candlepin_error_log)
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
        >>> candlepin_log.get('req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28')[0]['raw_message']
        '2016-09-07 18:07:53,688 [req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28, org=org_ray] ERROR org.candlepin.sync.Importer - Conflicts occurred during import that were'

        >>> candlepin_log.get_after(datetime(2016, 9, 7, 16, 0, 0)[0]['raw_message']
        '2016-09-07 16:49:24,650 [=, org=] WARN  org.apache.qpid.transport.network.security.ssl.SSLUtil - Exception received while trying to verify hostname'
    """
    pass


@parser(Specs.foreman_ssl_access_ssl_log)
class ForemanSSLAccessLog(LogFileOutput):
    """Class for parsing ``var/log/httpd/foreman-ssl_access_ssl.log`` file.

    Sample log contents::

        10.181.73.211 - rhcapkdc.lmig.com [27/Mar/2017:13:34:52 -0400] "GET /rhsm/consumers/385e688f-43ad-41b2-9fc7-593942ddec78 HTTP/1.1" 200 10736 "-" "-"
        10.181.73.211 - rhcapkdc.lmig.com [27/Mar/2017:13:34:52 -0400] "GET /rhsm/status HTTP/1.1" 200 263 "-" "-"
        10.185.73.33 - 8a31cd915917666001591d6fb44602a7 [27/Mar/2017:13:34:52 -0400] "GET /pulp/repos/Liberty_Mutual_Holding_Company_Inc/Library/RHEL7_Sat_Cap        sule_Servers/content/dist/rhel/server/7/7Server/x86_64/os/repodata/repomd.xml HTTP/1.1" 200 2018 "-" "urlgrabber/3.10 yum/3.4.3"
        10.181.73.211 - rhcapkdc.lmig.com [27/Mar/2017:13:34:52 -0400] "GET /rhsm/consumers/4f8a39d0-38b6-4663-8b7e-03368be4d3ab/owner HTTP/1.1" 200 5159 "-"
        10.181.73.211 - rhcapkdc.lmig.com [27/Mar/2017:13:34:52 -0400] "GET /rhsm/consumers/385e688f-43ad-41b2-9fc7-593942ddec78/compliance HTTP/1.1" 200 5527
        10.181.73.211 - rhcapkdc.lmig.com [27/Mar/2017:13:34:52 -0400] "GET /rhsm/consumers/4f8a39d0-38b6-4663-8b7e-03368be4d3ab HTTP/1.1" 200 10695 "-" "-"


    Examples:
        >>> foreman_ssl_acess_log = shared[ForemanSSLAccessLog]
        >>> foreman_ssl_acess_log.get('req=d9dc3cfd-abf7-485e-b1eb-e1e28e4b0f28')
    """
    time_format = '%d/%b/%Y:%H:%M:%S'
