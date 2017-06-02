"""
Combiner for httpd configurations
=======================================

Combiner for parsing part of httpd configurations. It collects all
HttpdConf generated from each httpd configuration files and get the valid
settings by sorting the file's in alphanumeric order. It provides an interface
to get the valid value of specific directive.

It also correctly handles position of ``IncludeOptional conf.d/*.conf`` line.

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
    >>> htd_conf.get_valid_setting_full("DocumentRoot")
    ParsedData('/var/www/html', 'DocumentRoot "/var/www/html"', '00-z.conf', '/etc/httpd/conf.d/00-z.conf')
"""
from collections import namedtuple

from insights.core.plugins import combiner
from insights.parsers.httpd_conf import HttpdConf


@combiner(requires=[HttpdConf])
class HttpdConfAll(object):
    """
    A combiner for parsing all httpd configurations. It parses all sources and makes a composition
    to store actual loaded values of the settings as well as information about parsed configuration
    files and raw values.

    Note:
        ``ParsedData`` is a named tuple with the following properties:
            - ``value`` - the value of the option.
            - ``line`` - the complete line as found in the config file.
            - ``file_name`` - the config file name.
            - ``file_path`` - the complete config file path.

        ``ConfigData`` is a named tuple with the following properties:
            - ``file_name`` - the config file name.
            - ``file_path`` - the complete config file path.
            - ``data_dict`` - original full_data dictionary from parser.

    Attributes:
        data (dict): Dictionary of parsed settings in format {option: [ParsedData, ParsedData]}.
                     It stores a list of parsed values, usually only the last value is needed,
                     except situations when directives which can use selective overriding,
                     such as ``UserDir``, are used.
        config_data (list): List of parsed config files in containing ConfigData named tuples.
    """
    ParsedData = namedtuple('ParsedData', ['value', 'line', 'file_name', 'file_path'])
    ConfigData = namedtuple('ConfigData', ['file_name', 'file_path', 'full_data_dict'])

    def __init__(self, local, shared):
        self.data = {}
        self.config_data = []

        config_files_data = []
        main_config_data = []

        for httpd_parser in shared[HttpdConf]:
            file_name = httpd_parser.file_name
            file_path = httpd_parser.file_path

            # Flag to be used for different handling of the main config file
            main_config = httpd_parser.file_name == 'httpd.conf'

            if not main_config:
                config_files_data.append(self.ConfigData(file_name, file_path,
                                                         httpd_parser.full_data))
            else:
                main_config_data.append(self.ConfigData(file_name, file_path,
                                                        httpd_parser.first_half))
                main_config_data.append(self.ConfigData(file_name, file_path,
                                                        httpd_parser.second_half))

        # Sort configuration files
        config_files_data.sort()

        # Add both parts of main configuration file and store as attribute.
        # These values can be used when looking for bad settings which are not actually active
        # but may become active if other configurations are changed
        if main_config_data:
            self.config_data = [main_config_data[0]] + config_files_data + [main_config_data[1]]
        else:
            self.config_data = config_files_data

        # Store active settings - the last parsed value us stored
        for file_name, file_path, full_data in self.config_data:
            for option, parsed_data in full_data.iteritems():
                if isinstance(parsed_data, dict):
                    # For section
                    section = option
                    content = parsed_data
                    if section not in self.data:
                        self.data[section] = {}

                    for k, pd in content.iteritems():
                        values = [self.ParsedData(a.value, a.line, file_name, file_path)
                                  for a in pd]
                        self.data[section][k] = values
                else:
                    # For directive
                    values = [self.ParsedData(a.value, a.line, file_name, file_path)
                              for a in parsed_data]
                    self.data[option] = values

    def get_setting_list(self, directive, section=None):
        """
        Returns the parsed data of the specified directive as a list of named tuples.

        Parameters:
            directive (str): The directive to look for.
            section (str): The section if the directive belongs to one.

        Returns:
            (list): List of named tuples ParsedData, in order how they are parsed. If directive
                    does not exist, it returns None.
        """
        if section:
            return self.data.get(section, {}).get(directive)
        return self.data.get(directive)

    def get_active_setting(self, directive, section=None):
        """
        Return the active parsed setting of the specified directive as a named tuple. It is the
        last parsed value and for most directives it is also the active setting.

        Parameters:
            directive (str): The directive to look for.
            section (str): The section if the directive belongs to one.

        Returns:
            (namedtuple): Named tuple ParsedData if directive exists, else None.
        """
        values_list = self.get_setting_list(directive, section)
        if values_list is None:
            return None
        else:
            return values_list[-1]

    def get_valid_setting(self, directive, section=None):
        """
        Return the active parsed setting of the specified directive. It is the last parsed value
        and for most directives it is also the active setting.

        Parameters:
            directive (str): The directive to look for.
            section (str): The section if the directive belongs to one.

        Returns:
            (tuple): ('the value of the directive', 'the configuration file') if directive exists,
                     else None.

        Note:
            This method is deprecated and should be removed in the future. Use
            ``get_active_setting`` instead. The word 'valid' in the method name is misleading.
        """
        valid_setting = self.get_active_setting(directive, section)
        if valid_setting is None:
            return None
        else:
            return valid_setting.value, valid_setting.file_name
