from .. import MapperOutput, mapper, computed

import xml.etree.ElementTree as ET


@mapper("cib.xml")
class CIB(MapperOutput):
    """
    Wraps a DOM of cib.xml

    self.dom is an instance of ElementTree.
    """

    def __init__(self, data, path=None):
        self.dom = ET.fromstring(data)
        super(CIB, self).__init__(data, path)

    @staticmethod
    def parse_content(content):
        return "\n".join(content)

    @computed
    def nodes(self):
        return [n.get("uname").lower() for n in self.dom.findall(".//nodes/node")]
