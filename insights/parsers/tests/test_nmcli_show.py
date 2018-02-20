import pytest
from insights.tests import context_wrap
from insights.parsers.nmcli_show import NmcliDevShow

NMCLI_SHOW = """
GENERAL.DEVICE:                         em3
GENERAL.TYPE:                           ethernet
GENERAL.HWADDR:                         B8:2A:72:DE:F8:B9
GENERAL.MTU:                            1500
GENERAL.STATE:                          100 (connected)
GENERAL.CONNECTION:                     em3
GENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/1
WIRED-PROPERTIES.CARRIER:               on
IP4.ADDRESS[1]:                         10.16.184.98/22
IP4.GATEWAY:                            10.16.187.254
IP4.DNS[1]:                             10.16.36.29
IP4.DNS[2]:                             10.11.5.19
IP4.DNS[3]:                             10.5.30.160
IP4.DOMAIN[1]:                          khw.lab.eng.bos.redhat.com
IP6.ADDRESS[1]:                         2620:52:0:10bb:ba2a:72ff:fede:f8b9/64
IP6.ADDRESS[2]:                         fe80::ba2a:72ff:fede:f8b9/64
IP6.GATEWAY:                            fe80:52:0:10bb::fc
IP6.ROUTE[1]:                           dst = 2620:52:0:10bb::/64, nh = ::, mt = 100

GENERAL.DEVICE:                         em1
GENERAL.TYPE:                           ethernet
GENERAL.HWADDR:                         B8:2A:72:DE:F8:BB
GENERAL.MTU:                            1500
GENERAL.STATE:                          30 (disconnected)
GENERAL.CONNECTION:                     --
GENERAL.CON-PATH:                       --
WIRED-PROPERTIES.CARRIER:               off

GENERAL.DEVICE:                         em2
GENERAL.TYPE:                           ethernet
GENERAL.HWADDR:                         B8:2A:72:DE:F8:BC
GENERAL.MTU:                            1500
GENERAL.STATE:                          30 (disconnected)
GENERAL.CONNECTION:                     --
GENERAL.CON-PATH:                       --
WIRED-PROPERTIES.CARRIER:               off
"""
def test_nmcli_show():
    nmcli_obj = NmcliDevShow(context_wrap(NMCLI_SHOW))

