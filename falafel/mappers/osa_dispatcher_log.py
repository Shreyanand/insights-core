from falafel.core.plugins import mapper
from falafel.core import LogFileOutput

from datetime import datetime
import re

"""
OSA-dispatcher log:
2015/12/23 04:40:58 -04:00 28307 0.0.0.0: osad/jabber_lib.__init__
2015/12/23 04:40:58 -04:00 28307 0.0.0.0: osad/jabber_lib.setup_connection('Connected to jabber server', u'example.com')
2015/12/23 04:40:58 -04:00 28307 0.0.0.0: osad/osa_dispatcher.fix_connection('Upstream notification server started on port', 1290)
2015/12/23 04:40:58 -04:00 28307 0.0.0.0: osad/jabber_lib.process_forever
2015/12/27 22:48:50 -04:00 28307 0.0.0.0: osad/jabber_lib.main('ERROR', 'Error caught:')
2015/12/27 22:48:50 -04:00 28307 0.0.0.0: osad/jabber_lib.main('ERROR', 'Traceback (most recent call last):\n  File "/usr/share/rhn/osad/jabber_lib.py", line 121, in main\n    self.process_forever(c)\n  File "/usr/share/rhn/osad/jabber_lib.py", line 179, in process_forever\n    self.process_once(client)\n  File "/usr/share/rhn/osad/osa_dispatcher.py", line 187, in process_once\n    client.retrieve_roster()\n  File "/usr/share/rhn/osad/jabber_lib.py", line 729, in retrieve_roster\n    stanza = self.get_one_stanza()\n  File "/usr/share/rhn/osad/jabber_lib.py", line 801, in get_one_stanza\n    self.process(timeout=tm)\n  File "/usr/share/rhn/osad/jabber_lib.py", line 1063, in process\n    self._parser.Parse(data)\n  File "/usr/lib/python2.6/site-packages/jabber/xmlstream.py", line 269, in unknown_endtag\n    self.dispatch(self._mini_dom)\n  File "/usr/share/rhn/osad/jabber_lib.py", line 829, in _orig_dispatch\n    jabber.Client.dispatch(self, stanza)\n  File "/usr/lib/python2.6/site-packages/jabber/jabber.py", line 290, in dispatch\n    else: handler[\'func\'](self,stanza)\n  File "/usr/share/rhn/osad/jabber_lib.py", line 380, in dispatch\n    callback(client, stanza)\n  File "/usr/share/rhn/osad/dispatcher_client.py", line 145, in _message_callback\n    sig = self._check_signature_from_message(stanza, actions)\n  File "/usr/share/rhn/osad/jabber_lib.py", line 1325, in _check_signature_from_message\n    sig = self._check_signature(stanza, actions=actions)\n  File "/usr/share/rhn/osad/dispatcher_client.py", line 69, in _check_signature\n    row = lookup_client_by_name(x_client_id)\n  File "/usr/share/rhn/osad/dispatcher_client.py", line 213, in lookup_client_by_name\n    raise InvalidClientError(client_name)\nInvalidClientError: 870d55ffbb949fae\n')

Works a bit like the XMLRPC log but I think the IP address is always 0.0.0.0
and the module is always 'osad' - it's more like what produced the log.
"""


@mapper('osa_dispatcher.log')
class OSADispatcherLog(LogFileOutput):

    LINE_STR = r"^(?P<timestamp>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} " + \
        r"[+-]?\d{2}:\d{2}) (?P<pid>\d+) (?P<client_ip>\S+): " + \
        r"(?P<module>\w+)/(?P<function>[\w_.-]+)(?:\((?P<info>.*)\))?$"
    LINE_RE = re.compile(LINE_STR)
    GROUPS = ('timestamp', 'pid', 'client_ip', 'module', 'function', 'info')

    def parse_line(self, line):
        """
            Parse a log line using the XMLRPC regular expression into a dict.
            All data will be in fields, and the raw log line is stored in
            'raw_log'.

            This also attempts to convert the timestamp given into a datetime
            object; if it can't convert it, then you don't get a 'datetime'
            key in the line's dict.
        """
        msg_info = dict()
        msg_info['raw_log'] = line

        match = self.LINE_RE.search(line)
        if match:
            for group in self.GROUPS:
                msg_info[group] = match.group(group)
            try:
                stamp = match.group('timestamp')
                # Must remove : from timezone for strptime %z
                msg_info['datetime'] = datetime.strptime(
                    stamp[0:23] + stamp[24:26], '%Y/%m/%d %H:%M:%S %z')
            except:
                pass

        return msg_info

    def get_parsed_lines(self, s):
        """
        Returns all lines that contain 's' anywhere and wrap them in a list
        """
        return [self.parse_line(l) for l in self.lines if s in l]

    def last(self):
        """
        Returns the last complete log line
        If the last line is not complete, then return the second last line
        """
        msg_info = dict()
        # Only check the last 2 lines, in that order
        for l in reversed(self.lines[-2:]):
            msg_info = self.parse_line(l)
            # assume parse is successful if we got an IP address
            if msg_info['client_ip']:
                return msg_info
        # Return the last one even if it didn't parse.
        return msg_info
