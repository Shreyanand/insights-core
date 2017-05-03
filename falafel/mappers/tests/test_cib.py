from falafel.mappers.cib import CIB
from falafel.tests import context_wrap

import unittest

CIB_CONFIG = """
    <cib crm_feature_set="3.0.9" validate-with="pacemaker-2.3" have-quorum="1" dc-uuid="4">
      <configuration>
        <crm_config>
          <cluster_property_set id="cib-bootstrap-options">
            <nvpair id="cib-bootstrap-options-have-watchdog" name="have-watchdog" value="false"/>
            <nvpair id="cib-bootstrap-options-no-quorum-policy" name="no-quorum-policy" value="freeze"/>
          </cluster_property_set>
        </crm_config>
        <nodes>
          <node id="1" uname="odchw1"/>
          <node id="2" uname="pyatt"/>
          <node id="3" uname="ford"/>
        </nodes>
        <resources>
          <clone id="dlm-clone">
          </clone>
        </resources>
        <constraints>
          <rsc_order first="dlm-clone" first-action="start" id="order-dlm-clone-clvmd-clone-mandatory" then="clvmd-clone" then-action="start"/>
          <rsc_colocation id="colocation-clvmd-clone-dlm-clone-INFINITY" rsc="clvmd-clone" score="INFINITY" with-rsc="dlm-clone"/>
        </constraints>
      </configuration>
    </cib>
"""


class TestCIB(unittest.TestCase):

    def test_cib(self):
        cib = CIB(context_wrap(CIB_CONFIG))
        self.assertTrue(cib)
        self.assertEqual(cib.nodes, ['odchw1', 'pyatt', 'ford'])
