from falafel.mappers.httpd_conf import HttpdConf
from falafel.tests import context_wrap

HTTPD_CONF_1 = """
SSLProtocol -ALL +SSLv3
#SSLProtocol all -SSLv2

NSSProtocol SSLV3 TLSV1.0
#NSSProtocol ALL

# prefork MPM
 <IfModule prefork.c>
StartServers       8
MinSpareServers    5
MaxSpareServers   20
ServerLimit      256
MaxClients       256
MaxRequestsPerChild  200
 </IfModule>

# worker MPM
<IfModule worker.c>
StartServers         4
MaxClients         300
MinSpareThreads     25
MaxSpareThreads     75
ThreadsPerChild     25
MaxRequestsPerChild  0
</IfModule>
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

HttpdConf.filters.extend([
    'SSLProtocol', 'NSSProtocol', 'RequestHeader', 'FcgidPassHeader'
    '<IfModule worker.c>', '<IfModule prefork.c>', '</IfModule>', 'MaxClients'
])


def test_get_filter_string_1():
    context = context_wrap(HTTPD_CONF_1, path=HTTPD_CONF_PATH)
    result = HttpdConf(context)

    assert result.data["SSLProtocol"] == "-ALL +SSLv3"
    assert "SSLCipherSuite" not in result.data
    assert "SSLV3 TLSV1.0" in result.data["NSSProtocol"]
    assert result.data["MPM_prefork"]["MaxClients"] == "256"
    assert result.data.get("MPM_worker")["MaxClients"] == "300"
    assert result.file_path == HTTPD_CONF_PATH
    assert result.file_name == "httpd.conf"


def test_get_filter_string_2():
    context = context_wrap(HTTPD_CONF_D_1, path=HTTPD_CONF_D_PATH)
    result = HttpdConf(context)

    except_SSLC = 'ALL:!ADH:!EXPORT:!SSLv2:RC4+RSA:+HIGH:+MEDIUM:+LOW'
    assert result.data["SSLProtocol"] == "-ALL +SSLv3"
    assert result.data["SSLCipherSuite"] == except_SSLC
    assert "NSSProtocol" not in result.data
    assert "MaxClients" not in result.data
    assert result.file_path == HTTPD_CONF_D_PATH
    assert result.file_name == "default.conf"
