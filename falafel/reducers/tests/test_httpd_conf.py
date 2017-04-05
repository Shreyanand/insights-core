from falafel.mappers.httpd_conf import HttpdConf
from falafel.reducers.httpd_conf import HttpdConfAll
from falafel.tests import context_wrap

HTTPD_CONF_1 = '''
JustFotTest_NoSec "/var/www/cgi"
# prefork MPM
<IfModule prefork.c>
ServerLimit      256
ThreadsPerChild  16
JustForTest      "AB"
MaxClients       256
</IfModule>
'''.strip()

HTTPD_CONF_2 = '''
JustForTest_NoSec "/var/www/cgi"
# prefork MPM
<IfModule prefork.c>
ServerLimit      1024
JustForTest      "ABC"
MaxClients       1024
</IfModule>
'''.strip()

HTTPD_CONF_3 = '''
# prefork MPM
<IfModule prefork.c>
ServerLimit      256
MaxClients       512
</IfModule>
'''.strip()


def test_valid_httpd():
    httpd1 = HttpdConf(context_wrap(HTTPD_CONF_1, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = HttpdConf(context_wrap(HTTPD_CONF_2, path='/etc/httpd/conf.d/00-z.conf'))
    httpd3 = HttpdConf(context_wrap(HTTPD_CONF_3, path='/etc/httpd/conf.d/z-z.conf'))
    shared = {HttpdConf: [httpd1, httpd2, httpd3]}
    result = HttpdConfAll(None, shared)
    assert result.get_valid_setting('MaxClients', 'MPM_prefork') == ('512', 'z-z.conf')
    assert result.get_valid_setting('ThreadsPerChild', 'MPM_prefork') == ('16', 'httpd.conf')
    assert result.get_valid_setting('ServerLimit', 'MPM_prefork') == ('256', 'z-z.conf')
    assert result.get_valid_setting('JustForTest', 'MPM_prefork') == ('ABC', '00-z.conf')
    assert result.get_valid_setting('JustForTest_NoSec') == ('/var/www/cgi', '00-z.conf')
