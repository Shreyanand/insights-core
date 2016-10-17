from falafel.mappers.uname import uname
from falafel.tests import context_wrap
import falafel

UNAME1 = "Linux ceehadoop1.gsslab.rdu2.redhat.com 2.6.32-504.el6.x86_64 #1 SMP Tue Sep 16 01:56:35 EDT 2014 x86_64 x86_64 x86_64 GNU/Linux"
UNAME2 = "Linux rhel7box 3.10.0-229.el7.x86_64 #1 SMP Mon Mar 3 13:32:45 EST 2014 x86_64 x86_64 x86_64 GNU/Linux"
UNAME3 = "Linux map1a 2.6.18-53.el5PAE #1 SMP Wed Oct 10 16:48:18 EDT 2007 i686 i686 i386 GNU/Linux"
UNAME4 = "Linux cvlvtsmsrv01 3.10.0-229.el7.x86_64 #1 SMP Thu Jan 29 18:37:38 EST 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_1 = "Linux localhost.localdomain 2.6.24.7-101.el5rt.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_1pre = "Linux localhost.localdomain 2.6.24.6-101.el5rt.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_1pre2 = "Linux localhost.localdomain 2.6.24-101.el5.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_1post = "Linux localhost.localdomain 2.6.24.7-101.1.el5rt.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_1post2 = "Linux localhost.localdomain 2.6.25-101.el5.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_2 = "Linux localhost.localdomain 2.6.33.9-rt31.66.el6rt.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_2pre = "Linux localhost.localdomain 2.6.33.9-rt31.65.el6rt.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_2pre2 = "Linux localhost.localdomain 2.6.33-65.el6.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_2post = "Linux localhost.localdomain 2.6.34.1-rt31.65.el6rt.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_2post2 = "Linux localhost.localdomain 2.6.34-65.el6.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_3 = "Linux localhost.localdomain 3.10.0-327.rt56.204.el7.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_3pre = "Linux localhost.localdomain 3.10.0-326.rt56.204.el7.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_3pre2 = "Linux localhost.localdomain 3.9.1-327.204.el7.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_3post = "Linux localhost.localdomain 3.10.0-328.rt56.204.el7.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
UNAME_RT_3post2 = "Linux localhost.localdomain 3.10.1-327.204.el7.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"


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

        uname_rt_1 = falafel.mappers.uname.Uname(context_wrap(UNAME_RT_1))
        assert uname_rt_1
        assert uname_rt_1.version == "2.6.24.7"
        assert uname_rt_1._sv_version is None
        assert uname_rt_1._lv_version == "2.6.24.7"
        assert uname_rt_1.release == "101.el5rt"
        assert uname_rt_1.arch == "x86_64"
        assert uname_rt_1 == UNAME_RT_1
        assert uname_rt_1 == falafel.mappers.uname.Uname.from_uname_str(UNAME_RT_1)
        assert uname_rt_1 > UNAME_RT_1pre
        assert uname_rt_1 > UNAME_RT_1pre2
        assert uname_rt_1 < UNAME_RT_1post
        assert uname_rt_1 < UNAME_RT_1post2
        assert uname_rt_1.rhel_release == ['-1', '-1']

        uname_rt_2 = falafel.mappers.uname.Uname(context_wrap(UNAME_RT_2))
        assert uname_rt_2
        assert uname_rt_2.version == "2.6.33.9"
        assert uname_rt_2._sv_version is None
        assert uname_rt_2._lv_version == "2.6.33.9"
        assert uname_rt_2.release == "rt31.66.el6rt"
        assert uname_rt_2.arch == "x86_64"
        assert uname_rt_2 == UNAME_RT_2
        assert uname_rt_2 == falafel.mappers.uname.Uname.from_uname_str(UNAME_RT_2)
        assert uname_rt_2 > UNAME_RT_2pre
        assert uname_rt_2 > UNAME_RT_2pre2
        assert uname_rt_2 < UNAME_RT_2post
        assert uname_rt_2 < UNAME_RT_2post2
        assert uname_rt_2.rhel_release == ['-1', '-1']

        uname_rt_3 = falafel.mappers.uname.Uname(context_wrap(UNAME_RT_3))
        assert uname_rt_3
        assert uname_rt_3.version == "3.10.0"
        assert uname_rt_3._sv_version == "3.10.0"
        assert uname_rt_3._lv_version == "3.10.0"
        assert uname_rt_3.release == "327.rt56.204.el7"
        assert uname_rt_3.arch == "x86_64"
        assert uname_rt_3 == UNAME_RT_3
        assert uname_rt_3 == falafel.mappers.uname.Uname.from_uname_str(UNAME_RT_3)
        assert uname_rt_3 > UNAME_RT_3pre
        assert uname_rt_3 > UNAME_RT_3pre2
        assert uname_rt_3 < UNAME_RT_3post
        assert uname_rt_3 < UNAME_RT_3post2
        assert uname_rt_3.rhel_release == ['7', '2']
