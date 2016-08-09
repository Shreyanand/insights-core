from falafel.mappers import httpd_conf
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

httpd_conf.parse_httpd_conf.filters.extend([
    'SSLProtocol', 'NSSProtocol', 'RequestHeader', 'FcgidPassHeader'
    '<IfModule worker.c>', '<IfModule prefork.c>', '</IfModule>', 'MaxClients'
])


def test_get_filter_string_1():
    context = context_wrap(HTTPD_CONF_1, path=HTTPD_CONF_PATH)
    result = httpd_conf.parse_httpd_conf(context)

    assert result["SSLProtocol"] == ["-all", "+sslv3"]
    assert "SSLCipherSuite" not in result
    assert "sslv3 tlsv1.0" in result["NSSProtocol"]
    assert result["MPM_prefork"]["MaxClients"] == "256"
    assert result.get("MPM_worker")["MaxClients"] == "300"
    assert result.file_path == HTTPD_CONF_PATH
    assert result.file_name == "httpd.conf"


def test_get_filter_string_2():
    context = context_wrap(HTTPD_CONF_D_1, path=HTTPD_CONF_D_PATH)
    result = httpd_conf.parse_httpd_conf(context)

    except_SSLC = [
        "all",
        "!adh",
        "!export",
        "!sslv2",
        "rc4+rsa",
        "+high",
        "+medium",
        "+low",
    ]

    assert result["SSLProtocol"] == ["-all", "+sslv3"]
    assert result["SSLCipherSuite"] == except_SSLC
    assert "NSSProtocol" not in result
    assert "MaxClients" not in result
    assert result.file_path == HTTPD_CONF_D_PATH
    assert result.file_name == "default.conf"
