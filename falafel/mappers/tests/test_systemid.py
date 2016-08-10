from falafel.tests import context_wrap
from falafel.mappers.systemid import systemid

SYSTEMID = '''
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


class TestSystemId():
    def test_systemid(self):
        info = systemid(context_wrap(SYSTEMID,
                                     path='etc/sysconfig/rhn/systemid'))

        assert len(info.data) == 9
        assert info.data["username"] == 'johnsow1'
        assert info.data["operating_system"] == 'redhat-release-workstation'
        assert info.data["description"] == 'Initial Registration Parameters: OS: redhat-release-workstation Release: 6Workstation CPU Arch: x86_64'
        assert info.data["checksum"] == 'b493da72be7cfb7e54c1d58c6aa140c9'
        assert info.data["profile_name"] == 'usorla7hr0107x'
        assert info.data["system_id"] == 'ID-1000030112'
        assert info.data["architecture"] == 'x86_64'
        assert info.data["os_release"] == '6Workstation'
        assert info.data["type"] == 'REAL'

        assert info.file_name == 'systemid'
        assert info.file_path == 'etc/sysconfig/rhn/systemid'
