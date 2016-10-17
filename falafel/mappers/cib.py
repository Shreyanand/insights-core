from .. import Mapper, mapper

import xml.etree.ElementTree as ET


@mapper("cib.xml")
class CIB(Mapper):
    """
    Wraps a DOM of cib.xml

    self.dom is an instance of ElementTree.
    """
    def parse_content(self, content):
        self.dom = ET.fromstring("\n".join(content))

    @property
    def nodes(self):
        return [n.get("uname").lower() for n in self.dom.findall(".//nodes/node")]
