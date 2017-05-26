from insights.mappers.hponcfg import HponConf
from insights.tests import context_wrap

HPONCFG = """
HP Lights-Out Online Configuration utility
Version 4.3.1 Date 05/02/2014 (c) Hewlett-Packard Company, 2014
Firmware Revision = 1.40 Device type = iLO 4 Driver name = hpilo
Host Information:
                        Server Name: esxi01.hp.local
                        Server Number:
"""


def test_hponcfg():

    conf = HponConf(context_wrap(HPONCFG))

    assert "1.40" == conf.firmware_revision
    assert "iLO 4" == conf.device_type
    assert "hpilo" == conf.driver_name
    assert "esxi01.hp.local" == conf['server_name']
    assert "" == conf['server_number']
