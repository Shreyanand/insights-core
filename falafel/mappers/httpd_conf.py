"""
HttpdConf - files ``/etc/httpd/conf/httpd.conf`` and ``/etc/httpd/conf.d/*``
============================================================================

Parse the keyword-and-value-but-also-vaguely-XML of an Apache configuration
file.

Generally, each line is split on the first space into key and value, leading
and trailing space being ignored.  If the 'IfModule' declaration is found,
then the data in this section (i.e. up to the '</IfModule' line) is stored
under the 'MPM_prefork' key if the IfModule declaration contains 'prefork.c',
or the 'MPM_worker' key if the IfModule declaration contains 'worker.c'; if
neither is found the data in this IfModule is stored as if the IfModule
declaration did not exist.

**NB**: at this point in time, this does **not** attempt to provide any
semblance of structure to the configuration file.  It is really just a
simple key-value dictionary mapper, with a basic understanding of the IfModule
declaration for how Apache handles multiple requests.  In particular, you
**must** add filters to this mapper to find the lines you want, because lines
in this module are filtered.

Sample (edited) httpd.conf file::

    ServerRoot "/etc/httpd"
    LoadModule auth_basic_module modules/mod_auth_basic.so
    LoadModule auth_digest_module modules/mod_auth_digest.so

    <Directory />
        Options FollowSymLinks
        AllowOverride None
    </Directory>

    <IfModule mod_mime_magic.c>
    #   MIMEMagicFile /usr/share/magic.mime
        MIMEMagicFile conf/magic
    </IfModule>

    ErrorLog "|/usr/sbin/httplog -z /var/log/httpd/error_log.%Y-%m-%d"

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

Examples:

    >>> httpconf = shared[HttpdConf]
    >>> httpconf.data['ServerRoot'] # Quotes are not removed
    '"/etc/httpd"'
    >>> httpconf.data['LoadModule'] # Later declarations overwrite earlier
    'auth_digest_module modules/mod_auth_digest.so'
    >>> httpconf.data['Options'] # Sections are currently ignored
    'FollowSymLinks'
    >>> type(httpconf.data['MPM_prefork'])
    <type 'dict'>
    >>> httpconf.data['MPM_prefork']['StartServers'] # No type conversion
    '8'
    >>> 'ThreadsPerChild' in httpconf.data['MPM_prefork']
    False
    >>> httpconf.data['MPM_worker']['MaxRequestsPerChild']
    '0'

"""

import re
from .. import Mapper, mapper, get_active_lines, LegacyItemAccess


@mapper('httpd.conf', filters=['IncludeOptional'])
@mapper('httpd.conf.d')
class HttpdConf(LegacyItemAccess, Mapper):
    """
    Get the key value pairs separated on the first space, ignoring leading
    and trailing spaces.  The "<IfModule prefork.c>" and "<IfModule worker.c>"
    sections are parsed into 'MPM_prefork' and 'MPM_worker' sub-dictionaries
    respectively.

    If the file is ``httpd.conf``, it also stores first half, before
    ``IncludeOptional conf.d/*.conf`` line, and the rest, to the ``first_half``
    and ``second_half`` attributes respectively.
    """
    def __init__(self, *args, **kwargs):
        self.data = {}
        """dict: Dictionary of parsed data."""
        self.first_half = {}
        """dict: Parsed data from main config file before inclusion of other files."""
        self.second_half = {}
        """dict: Parsed data from main config file after inclusion of other files."""

        super(HttpdConf, self).__init__(*args, **kwargs)

    def parse_content(self, content):
        where_to_store = self.first_half  # Set which part of file is the parser at

        # Flag to be used for different parsing of the main config file
        main_config = self.file_name == 'httpd.conf'

        section = None
        for line in get_active_lines(content):
            if main_config and where_to_store is not self.second_half:
                # Dividing line looks like 'IncludeOptional conf.d/*.conf'
                if re.search(r'^\s*IncludeOptional\s+conf\.d', line):
                    where_to_store = self.second_half

            # new IfModule section start
            if line.startswith('<IfModule'):
                section = "MPM_{}".format(line.split()[-1].split('.')[0].lower())
            # section end
            elif line.startswith('</IfModule'):
                section = None
            else:
                try:
                    option, value = [s.strip() for s in line.split(None, 1)]
                except ValueError:
                    continue  # Skip lines which are not 'Option Value'
                value = value.strip('\'"')
                if section:
                    if section not in self.data:
                        self.data[section] = {option: value}
                        if main_config:
                            where_to_store[section] = {option: value}
                    else:
                        self.data[section][option] = value
                        if main_config:
                            where_to_store[section][option] = value
                else:
                    self.data[option] = value
                    if main_config:
                        where_to_store[option] = value
