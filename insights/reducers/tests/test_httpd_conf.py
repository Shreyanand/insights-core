from insights.mappers.httpd_conf import HttpdConf
from insights.reducers.httpd_conf import HttpdConfAll
from insights.tests import context_wrap

HTTPD_CONF_1 = '''
JustFotTest_NoSec "/var/www/cgi"
# prefork MPM
<IfModule prefork.c>
ServerLimit      256
ThreadsPerChild  16
JustForTest      "AB"
MaxClients       256
</IfModule>

IncludeOptional conf.d/*.conf
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


HTTPD_CONF_MAIN_1 = '''
ServerRoot "/etc/httpd"
Listen 80

# Load config files in the "/etc/httpd/conf.d" directory, if any.
IncludeOptional conf.d/*.conf
'''.strip()

HTTPD_CONF_MAIN_2 = '''
# Load config files in the "/etc/httpd/conf.d" directory, if any.
IncludeOptional conf.d/*.conf

ServerRoot "/etc/httpd"
Listen 80
'''.strip()

HTTPD_CONF_MAIN_3 = '''
ServerRoot "/etc/httpd"

# Load config files in the "/etc/httpd/conf.d" directory, if any.
IncludeOptional conf.d/*.conf

Listen 80
'''.strip()

HTTPD_CONF_FILE_1 = '''
ServerRoot "/home/skontar/httpd"
Listen 8080
'''.strip()

HTTPD_CONF_FILE_2 = '''
ServerRoot "/home/skontar/www"
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

    assert result.get_valid_setting_full('MaxClients', 'MPM_prefork').file_path == '/etc/httpd/conf.d/z-z.conf'


def test_httpd_splits():
    httpd1 = HttpdConf(context_wrap(HTTPD_CONF_MAIN_1, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = HttpdConf(context_wrap(HTTPD_CONF_FILE_1, path='/etc/httpd/conf.d/00-a.conf'))
    httpd3 = HttpdConf(context_wrap(HTTPD_CONF_FILE_2, path='/etc/httpd/conf.d/01-b.conf'))
    shared = {HttpdConf: [httpd1, httpd2, httpd3]}
    result = HttpdConfAll(None, shared)
    assert result.get_valid_setting_full('ServerRoot').value == '/home/skontar/www'
    assert result.get_valid_setting_full('ServerRoot').line == 'ServerRoot "/home/skontar/www"'
    assert result.get_valid_setting_full('ServerRoot').file_name == '01-b.conf'
    assert result.get_valid_setting_full('ServerRoot').file_path == '/etc/httpd/conf.d/01-b.conf'
    assert result.get_valid_setting_full('Listen').value == '8080'
    assert result.get_valid_setting_full('Listen').line == 'Listen 8080'
    assert result.get_valid_setting_full('Listen').file_name == '00-a.conf'
    assert result.get_valid_setting_full('Listen').file_path == '/etc/httpd/conf.d/00-a.conf'

    httpd1 = HttpdConf(context_wrap(HTTPD_CONF_MAIN_2, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = HttpdConf(context_wrap(HTTPD_CONF_FILE_1, path='/etc/httpd/conf.d/00-a.conf'))
    httpd3 = HttpdConf(context_wrap(HTTPD_CONF_FILE_2, path='/etc/httpd/conf.d/01-b.conf'))
    shared = {HttpdConf: [httpd1, httpd2, httpd3]}
    result = HttpdConfAll(None, shared)
    assert result.get_valid_setting_full('ServerRoot').value == '/etc/httpd'
    assert result.get_valid_setting_full('ServerRoot').line == 'ServerRoot "/etc/httpd"'
    assert result.get_valid_setting_full('ServerRoot').file_name == 'httpd.conf'
    assert result.get_valid_setting_full('ServerRoot').file_path == '/etc/httpd/conf/httpd.conf'
    assert result.get_valid_setting_full('Listen').value == '80'
    assert result.get_valid_setting_full('Listen').line == 'Listen 80'
    assert result.get_valid_setting_full('Listen').file_name == 'httpd.conf'
    assert result.get_valid_setting_full('Listen').file_path == '/etc/httpd/conf/httpd.conf'

    httpd1 = HttpdConf(context_wrap(HTTPD_CONF_MAIN_3, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = HttpdConf(context_wrap(HTTPD_CONF_FILE_1, path='/etc/httpd/conf.d/00-a.conf'))
    httpd3 = HttpdConf(context_wrap(HTTPD_CONF_FILE_2, path='/etc/httpd/conf.d/01-b.conf'))
    shared = {HttpdConf: [httpd1, httpd2, httpd3]}
    result = HttpdConfAll(None, shared)
    assert result.get_valid_setting_full('ServerRoot').value == '/home/skontar/www'
    assert result.get_valid_setting_full('ServerRoot').line == 'ServerRoot "/home/skontar/www"'
    assert result.get_valid_setting_full('ServerRoot').file_name == '01-b.conf'
    assert result.get_valid_setting_full('ServerRoot').file_path == '/etc/httpd/conf.d/01-b.conf'
    assert result.get_valid_setting_full('Listen').value == '80'
    assert result.get_valid_setting_full('Listen').line == 'Listen 80'
    assert result.get_valid_setting_full('Listen').file_name == 'httpd.conf'
    assert result.get_valid_setting_full('Listen').file_path == '/etc/httpd/conf/httpd.conf'

    # Test is data from inactive configs are also stored
    assert [a.file_name for a in result.config_data] == ['httpd.conf', '00-a.conf', '01-b.conf', 'httpd.conf']
    assert result.config_data[1].file_name == '00-a.conf'
    assert result.config_data[1].file_path == '/etc/httpd/conf.d/00-a.conf'
    assert result.config_data[1].full_data_dict['Listen'].value == '8080'
    assert result.config_data[1].full_data_dict['Listen'].line == 'Listen 8080'


def test_httpd_no_main_config():
    httpd2 = HttpdConf(context_wrap(HTTPD_CONF_FILE_1, path='/etc/httpd/conf.d/00-a.conf'))
    httpd3 = HttpdConf(context_wrap(HTTPD_CONF_FILE_2, path='/etc/httpd/conf.d/01-b.conf'))
    shared = {HttpdConf: [httpd2, httpd3]}
    result = HttpdConfAll(None, shared)
    assert [a.file_name for a in result.config_data] == ['00-a.conf', '01-b.conf']
