"""
Shared reducer for httpd configurations
=======================================

Shared reducer for parsing part of httpd configurations. It collects all
HttpdConf generated from each httpd configuration files and get the valid
settings by sorting the file's in alphanumeric order. It provides an interface
to get the valid value of specific directive.


Examples:
    >>> HTTPD_CONF_1 = '''
    ... # prefork MPM
    ... DocumentRoot "/var/www/html_cgi"
    ... <IfModule prefork.c>
    ... ServerLimit      256
    ... MaxClients       256
    ... </IfModule>
    ... '''.strip()
    >>> HTTPD_CONF_2 = '''
    ... DocumentRoot "/var/www/html"
    ... # prefork MPM
    ... <IfModule prefork.c>
    ... ServerLimit      512
    ... MaxClients       512
    ... </IfModule>
    ... '''.strip()
    >>> httpd1 = HttpdConf(context_wrap(HTTPD_CONF, path='/etc/httpd/conf/httpd.conf'))
    >>> httpd2 = HttpdConf(context_wrap(HTTPD_CONF, path='/etc/httpd/conf.d/00-z.conf'))
    >>> shared = [{HttpdConf: [httpd1, httpd2]}]
    >>> htd_conf = shared[HttpdConfAll]
    >>> htd_conf.get_valid_setting("MaxClients", "MPM_prefork")
    ('512', '00-z.conf')
    >>> htd_conf.get_valid_setting("DocumentRoot")
    ('/var/www/html', '00-z.conf')
"""

from falafel.core.plugins import reducer
from falafel.mappers.httpd_conf import HttpdConf


class HttpConfAllReducer(object):
    """
    A reducer for parsing all httpd configurations
    """
    def __init__(self, local, shared):
        htp_inf = []
        def_inf = {}
        for htp in shared[HttpdConf]:
            fn = htp.file_name
            if fn == 'httpd.conf':
                def_inf = htp.data
            else:
                htp_inf.append({fn: htp.data})
        # Sort the configuration files
        htp_inf.sort()
        # httpd.conf is always the first one to check
        all_data = [{'httpd.conf': def_inf}]
        all_data.extend(htp_inf)
        # Get the valid setting for each directive from all `.conf` file in
        # files' alphanumerical order. And record the file's name.
        self.data = {}
        for file_conf in all_data:
            fn = file_conf.keys()[0]
            data = file_conf.values()[0]
            for dkey, dval in data.iteritems():
                if isinstance(dval, dict):
                    # For section
                    if dkey not in self.data:
                        self.data[dkey] = {}
                    for k, v in dval.iteritems():
                        self.data[dkey][k] = (v, fn)
                else:
                    # For directive
                    self.data[dkey] = (dval, fn)

    def get_valid_setting(self, directive, section=None):
        """
        Return the valid value of specified directive.

        Parameters:
            directive (str): The directive to look for.
            section (str): The section if the directive belongs to one.

        Returns:
            (tuple): ('the value of the directive', 'the configuration file')
        """
        if section:
            return self.data.get(section, {}).get(directive)
        return self.data.get(directive)


@reducer(requires=[HttpdConf], shared=True)
class HttpdConfAll(HttpConfAllReducer):
    """Class for collecting and sorting all the httpd configuration files"""
    pass
