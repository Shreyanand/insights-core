from falafel.tests import context_wrap
from falafel.mappers.rhn_logs import TaskomaticDaemonLog, SearchDaemonLog
from falafel.mappers.rhn_logs import ServerXMLRPCLog
from datetime import datetime


search_daemon_log = """
STATUS | wrapper  | 2013/01/28 14:22:38 | TERM trapped.  Shutting down.
STATUS | wrapper  | 2013/01/28 14:22:39 | <-- Wrapper Stopped
STATUS | wrapper  | 2013/01/28 14:41:58 | --> Wrapper Started as Daemon
STATUS | wrapper  | 2013/01/28 14:41:58 | Launching a JVM...
INFO   | jvm 1    | 2013/01/28 14:41:59 | Wrapper (Version 3.2.1) http://wrapper.tanukisoftware.org
STATUS | wrapper  | 2013/01/29 17:04:25 | TERM trapped.  Shutting down.
""".strip()

taskomatic_daemon_log = """
STATUS | wrapper  | 2016/05/18 15:13:36 | --> Wrapper Started as Daemon
STATUS | wrapper  | 2016/05/18 15:13:36 | Launching a JVM...
INFO   | jvm 1    | 2016/05/18 15:13:36 | Wrapper (Version 3.2.3) http://wrapper.tanukisoftware.org
INFO   | jvm 1    | 2016/05/18 15:13:36 |   Copyright 1999-2006 Tanuki Software, Inc.  All Rights Reserved.
INFO   | jvm 1    | 2016/05/18 15:13:39 | May 18, 2016 3:13:39 PM com.mchange.v2.log.MLog <clinit>
INFO   | jvm 1    | 2016/05/18 15:13:39 | INFO: MLog clients using java 1.4+ standard logging.
INFO   | jvm 1    | 2016/05/18 15:13:39 | May 18, 2016 3:13:39 PM com.mchange.v2.c3p0.C3P0Registry banner
INFO   | jvm 1    | 2016/05/18 15:13:39 | INFO: Initializing c3p0-0.9.1.2 [built 31-March-2011 15:45:28; debug? false; trace: 5]
INFO   | jvm 1    | 2016/05/18 15:13:39 | May 18, 2016 3:13:39 PM com.mchange.v2.c3p0.impl.AbstractPoolBackedDataSource getPoolManager
INFO   | jvm 1    | 2016/05/18 15:13:40 | INFO: Initializing c3p0 pool... com.mchange.v2.c3p0.PoolBackedDataSource@ea9d5b40
INFO   | jvm 1
""".strip()

SERVER_XMLRPC_LOG_DATA = """
2016/04/11 05:52:01 -04:00 23630 10.4.4.17: xmlrpc/registration.welcome_message('lang: None',)
2016/04/11 05:52:26 -04:00 12911 10.4.4.17: xmlrpc/registration.create_system("token = '1-RegKey'", '6Server', 'x86_64')
2016/04/11 05:52:26 -04:00 12911 10.4.4.17: rhnServer/server_token.process_token(1000010125, 'enterprise_entitled,provisioning_entitled,virtualization_host')
2016/04/11 05:52:47 -04:00 23628 10.4.4.17: xmlrpc/registration.__add_hw_profile_no_auth(1000010125, 'items: 6')
2016/04/11 10:49:12 -04:00 11594 192.168.18.163: xmlrpc/registration.welcome_message('lang: None',)
2016/04/11 10:49:12 -04:00 11601 192.168.18.163: xmlrpc/registration.register_osad
2016/04/11 10:49:17 -04:00 11599 192.168.18.163: xmlrpc/registration.register_osad_jid
2016/04/11 12:57:26 -04:00 11594 192.168.18.28: rhnServer/server_certificate.valid('Server id ID-1000010124 not found in database',)
2016/07/27 04:44:41 -04:00 25923 2620:10a:0:4::40: xmlrpc/queue.get(1000014812, 2, 'checkins enabled')
"""


def test_rhn_search_daemon_log():
    out_log = SearchDaemonLog(context_wrap(search_daemon_log))
    assert "Wrapper Started as Daemon" in out_log
    assert len(out_log.get("jvm")) == 1
    assert out_log.get("jvm")[0] == 'INFO   | jvm 1    | 2013/01/28 14:41:59 | Wrapper (Version 3.2.1) http://wrapper.tanukisoftware.org'


def test_rhn_taskomatic_daemon_log():
    out_log = TaskomaticDaemonLog(context_wrap(taskomatic_daemon_log))
    assert "Wrapper Started as Daemon" in out_log
    assert len(out_log.get("jvm")) == 9
    assert out_log.get("jvm")[2] == 'INFO   | jvm 1    | 2016/05/18 15:13:39 | May 18, 2016 3:13:39 PM com.mchange.v2.log.MLog <clinit>'
    assert out_log.last_log_date == datetime(2016, 5, 18, 15, 13, 40)


def test_server_xmlrpc_log_data():
    log = ServerXMLRPCLog(context_wrap(SERVER_XMLRPC_LOG_DATA))

    # Check the first log line for all fields
    line = log.get('10.4.4.17: xmlrpc/registration.welcome_message')[0]

    assert line['timestamp'] == '2016/04/11 05:52:01 -04:00'
    d = datetime(2016, 04, 11, 05, 52, 01)
    assert line['datetime'] == d
    assert line['pid'] == '23630'
    assert line['client_ip'] == '10.4.4.17'
    assert line['module'] == 'xmlrpc'
    assert line['function'] == 'registration.welcome_message'
    assert line['client_id'] is None
    assert line['args'] == "'lang: None'"

    # Check that get works
    assert len(log.get('welcome_message')) == 2

    # Check that __contains__ works
    assert 'welcome_message' in log

    # Check parsing of lines without argument lists
    line = log.get('registration.register_osad_jid')[0]
    assert line['args'] is None

    # Check lines that include the client ID
    line = log.get('__add_hw_profile_no_auth')[0]
    assert line['client_id'] == '1000010125'
    assert line['args'] == "'items: 6'"

    # Check that we can get IPv6 addresses correctly
    line = log.get('checkins enabled')[0]
    assert line['client_ip'] == '2620:10a:0:4::40'
    assert line['client_id'] == '1000014812'
    assert line['args'] == "2, 'checkins enabled'"
    # Use this line for the last test later

    # Test last attribute
    last = log.last
    assert line == last
