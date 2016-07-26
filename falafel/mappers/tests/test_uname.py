from falafel.mappers.uname import uname
from falafel.tests import context_wrap

UNAME1 = "Linux ceehadoop1.gsslab.rdu2.redhat.com 2.6.32-504.el6.x86_64 #1 SMP Tue Sep 16 01:56:35 EDT 2014 x86_64 x86_64 x86_64 GNU/Linux"
UNAME2 = "Linux rhel7box 3.10.0-229.el7.x86_64 #1 SMP Mon Mar 3 13:32:45 EST 2014 x86_64 x86_64 x86_64 GNU/Linux"
UNAME3 = "Linux map1a 2.6.18-53.el5PAE #1 SMP Wed Oct 10 16:48:18 EDT 2007 i686 i686 i386 GNU/Linux"
UNAME4 = "Linux cvlvtsmsrv01 3.10.0-229.el7.x86_64 #1 SMP Thu Jan 29 18:37:38 EST 2015 x86_64 x86_64 x86_64 GNU/Linux"


class TestUname(object):

    def test_uname(self):
        uname1 = uname(context_wrap(UNAME1))
        uname2 = uname(context_wrap(UNAME2))
        uname3 = uname(context_wrap(UNAME3))
        uname4 = uname(context_wrap(UNAME4))
        assert uname2.arch == 'x86_64'
        assert uname2 == uname4
        assert uname1 > uname3

        kernel1 = uname1
        assert [] == kernel1.fixed_by('2.6.32-220.1.el6', '2.6.32-504.el6')
        assert ['2.6.32-600.el6'] == kernel1.fixed_by('2.6.32-600.el6')
        assert [] == kernel1.fixed_by('2.6.32-600.el6', introduced_in='2.6.32-504.1.el6')
        assert ['2.6.33-100.el6'] == kernel1.fixed_by('2.6.33-100.el6')
        assert ['2.6.32-600.el6'] == kernel1.fixed_by('2.6.32-220.1.el6', '2.6.32-600.el6')
