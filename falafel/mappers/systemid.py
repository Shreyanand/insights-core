import xml.etree.ElementTree as ET
from .. import MapperOutput, mapper


@mapper('systemid')
class SystemID(MapperOutput):

    @staticmethod
    def parse_content(content):
        '''
        ---------------
        Return a SystemId object which contains a dict below:
            {
            "username": "johnsow1",
            "operating_system": "redhat-release-workstation",
            "description": "Initial Registration Parameters: OS: redhat-release-workstation Release: 6Workstation CPU Arch: x86_64",
            "checksum": "b493da72be7cfb7e54c1d58c6aa140c9",
            "profile_name": "usorla7hr0107x",
            "system_id": "ID-1000030112",
            "architecture": "x86_64",
            "os_release": "6Workstation",
            "type": "REAL"
            }
        Ignore the member with "fields" text. Because it's information is nonsense
        ---Sample---
        <?xml version="1.0"?>
        <params>
        <param>
        <value><struct>
        <member>
        <name>username</name>
        <value><string>johnsow1</string></value>
        </member>
        <member>
        <name>operating_system</name>
        <value><string>redhat-release-workstation</string></value>
        </member>
        <member>
        <name>description</name>
        <value><string>Initial Registration Parameters:
        OS: redhat-release-workstation
        Release: 6Workstation
        CPU Arch: x86_64</string></value>
        </member>
        <member>
        <name>checksum</name>
        <value><string>b493da72be7cfb7e54c1d58c6aa140c9</string></value>
        </member>
        <member>
        <name>profile_name</name>
        <value><string>usorla7hr0107x</string></value>
        </member>
        <member>
        <name>system_id</name>
        <value><string>ID-1000030112</string></value>
        </member>
        <member>
        <name>architecture</name>
        <value><string>x86_64</string></value>
        </member>
        <member>
        <name>os_release</name>
        <value><string>6Workstation</string></value>
        </member>
        <member>
        <name>fields</name>
        <value><array><data>
        <value><string>system_id</string></value>
        <value><string>os_release</string></value>
        <value><string>operating_system</string></value>
        <value><string>architecture</string></value>
        <value><string>username</string></value>
        <value><string>type</string></value>
        </data></array></value>
        </member>
        <member>
        <name>type</name>
        <value><string>REAL</string></value>
        </member>
        </struct></value>
        </param>
        </params>
        '''

        root = ET.fromstring('\n'.join(content))
        systemid_info = {}

        for member in root.findall(".//member"):
            # ignore "fields" infos
            if member[0].text != 'fields':
                key = member[0].text
                value = member[1][0].text
                systemid_info[key] = value
        return systemid_info
