"""
Pacemaker configuration - file ``/var/lib/pacemaker/cib/cib.xml``
=================================================================

This parser reads the XML in the Pacemaker configuration file and provides a
standard ElementTree interface to it.  It also provides a ``nodes`` property
that lists all the nodes.

Sample input::

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

Examples:

    >>> cib = shared(CIB)
    >>> opts = cib.dom.find(".//cluster_property_set[@id='cib-bootstrap-options']")
    >>> opts.get('id')
    'cib-bootstrap-options'
    >>> cib.nodes
    ['odchw1', 'pyatt', 'ford']

"""

from .. import Parser, parser

import xml.etree.ElementTree as ET
from insights.specs import cib_xml


@parser(cib_xml)
class CIB(Parser):
    """
    Wraps a DOM of cib.xml

    self.dom is an instance of ElementTree.
    """
    def parse_content(self, content):
        self.dom = ET.fromstring("\n".join(content))

    @property
    def nodes(self):
        """
        Fetch the list of nodes and return their unames as a list.
        """
        return [n.get("uname").lower() for n in self.dom.findall(".//nodes/node")]
