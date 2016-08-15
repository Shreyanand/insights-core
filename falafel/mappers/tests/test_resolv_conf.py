from falafel.mappers import resolv_conf
from falafel.tests import context_wrap


RESOLVCONF = '''
# This file is being maintained by Puppet.
# DO NOT EDIT
search a.b.com b.c.com
options timeout:2 attempts:2
nameserver 10.160.224.51
nameserver 10.160.225.51
nameserver 10.61.193.11
'''

RESOLVCONF_M = '''
# Generated by NetworkManager
search ttt.com
domain ttt.com
nameserver 192.168.30.1
'''


class TestResolvConf():
    def test_resolv_conf(self):
        resolv_info = resolv_conf.resolv_conf(context_wrap(RESOLVCONF))

        assert len(resolv_info.data) == 4

        assert resolv_info.data['search'] == ['a.b.com', 'b.c.com']
        assert resolv_info.data['options'] == ['timeout:2', 'attempts:2']
        assert resolv_info.data['nameserver'] == ['10.160.224.51', '10.160.225.51', '10.61.193.11']
        assert resolv_info.data['active'] == 'search'

    # Testing when 'search' and 'domain' keywords exit both.
    def test_resolv_conf_m(self):
        resolv_info = resolv_conf.resolv_conf(context_wrap(RESOLVCONF_M))

        assert len(resolv_info.data) == 4

        assert resolv_info.data['domain'] == ['ttt.com']
        assert resolv_info.data['search'] == ['ttt.com']
        assert resolv_info.data['nameserver'] == ['192.168.30.1']
        assert resolv_info.data['active'] == 'domain'
