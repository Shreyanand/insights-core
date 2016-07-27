import unittest

from falafel.mappers import httpd_conf
from falafel.tests import context_wrap

HTTPD_CONF_1 = """
SSLProtocol -ALL +SSLv3
#SSLProtocol all -SSLv2

NSSProtocol SSLV3 TLSV1.0
#NSSProtocol ALL

# MaxClients: maximum number of server processes allowed to start
   MaxClients          256

""".strip()

HTTPD_CONF_PATH = "etc/httpd/conf/httpd.conf"
HTTPD_CONF_D_PATH = "etc/httpd/conf.d/default.conf"

HTTPD_CONF_D_1 = """
SSLProtocol -ALL +SSLv3
#SSLProtocol all -SSLv2

#SSLCipherSuite ALL:!ADH:!EXPORT:!SSLv2:RC4+RSA:+HIGH:+MEDIUM:+LOW
SSLCipherSuite ALL:!ADH:!EXPORT:!SSLv2:RC4+RSA:+HIGH:+MEDIUM:+LOW

# MaxClients: maximum number of server processes allowed to start
   MaxClients
""".strip()

SSLP_string = "SSLProtocol"
SSLC_string = "SSLCipherSuite"
NSS_string = "NSSProtocol"
MaxClient_string = "MaxClients"


class TestHttpdConf(unittest.TestCase):
    def test_get_filter_string_1(self):
        context = context_wrap(HTTPD_CONF_1, path=HTTPD_CONF_PATH)
        result = httpd_conf.parse_httpd_conf(context)

        expect_SSLP = ["-all +sslv3"]
        expect_NSS = "sslv3 tlsv1.0"
        expect_MaxClient = ["256"]

        assert result.get_filter_strings(SSLP_string) == expect_SSLP
        assert not result.get_filter_strings(SSLC_string)
        assert expect_NSS in result.get_filter_strings(NSS_string)
        assert result.get_filter_strings(MaxClient_string) == expect_MaxClient
        assert result.file_path == HTTPD_CONF_PATH
        assert result.file_name == "httpd.conf"

    def test_get_filter_string_2(self):
        context = context_wrap(HTTPD_CONF_D_1, path=HTTPD_CONF_D_PATH)
        result = httpd_conf.parse_httpd_conf(context)

        expect_SSLP = ["-all +sslv3"]
        except_SSLC = ["all:!adh:!export:!sslv2:rc4+rsa:+high:+medium:+low"]

        assert result.get_filter_strings(SSLP_string) == expect_SSLP
        assert result.get_filter_strings(SSLC_string) == except_SSLC
        assert not result.get_filter_strings(NSS_string)
        assert not result.get_filter_strings(MaxClient_string)
        assert result.file_path == HTTPD_CONF_D_PATH
        assert result.file_name == "default.conf"
