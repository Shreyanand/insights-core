from insights.parsers import ovs_vsctl_show
from insights.tests import context_wrap

import doctest


OVS_VSCTL_SHOW_DOCS = '''
aa3f16d3-9534-4b74-8e9e-8b0ce94038c5
    Bridge br-int
        fail_mode: secure
        Port br-int
            Interface br-int
                type: internal
        Port int-br-ctlplane
            Interface int-br-ctlplane
            type: patch
            options: {peer=phy-br-ctlplane}
        Port "tap293d29ec-d1"
            tag: 1
            Interface "tap293d29ec-d1"
                type: internal
    Bridge br-tun
        fail_mode: secure
        Port "vxlan-aca80118"
            Interface "vxlan-aca80118"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="172.168.1.26", out_key=flow, remote_ip="172.168.1.24"}
        Port "vxlan-aca80119"
            Interface "vxlan-aca80119"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="172.168.1.26", out_key=flow, remote_ip="172.168.1.25"}
ovs_version: "2.3.2"
'''.strip()


def test_ovs_vsctl_show_documentation():
    env = {
        'OVSvsctlshow': ovs_vsctl_show.OVSvsctlshow,
        'shared': {
            ovs_vsctl_show.OVSvsctlshow: ovs_vsctl_show.OVSvsctlshow(
                context_wrap(OVS_VSCTL_SHOW_DOCS)
            ),
        }
    }
    failed, total = doctest.testmod(ovs_vsctl_show, globs=env)
    assert failed == 0


ovs_vsctl_show_output = """
e4d4f521-086d-4479-a88f-d531cd1646b8
    Bridge br-ex
        Port br-ex
            Interface br-ex
                type: internal
        Port "qg-dacc6089-be"
            Interface "qg-dacc6089-be"
                type: internal
        Port "eth0"
            Interface "eth0"
        Port phy-br-ex
            Interface phy-br-ex
                type: patch
                options: {peer=int-br-ex}
    Bridge br-int
        fail_mode: secure
        Port "tapfcce898c-ca"
            tag: 1
            Interface "tapfcce898c-ca"
                type: internal
        Port int-br-ex
            Interface int-br-ex
                type: patch
                options: {peer=phy-br-ex}
        Port "tapdf2d6113-b2"
            tag: 2
            Interface "tapdf2d6113-b2"
                type: internal
        Port patch-tun
            Interface patch-tun
                type: patch
                options: {peer=patch-int}
        Port br-int
            Interface br-int
                type: internal
        Port "ha-1f423581-cd"
            tag: 3
            Interface "ha-1f423581-cd"
                type: internal
        Port "qr-417e232b-dd"
            tag: 1
            Interface "qr-417e232b-dd"
                type: internal
    Bridge br-tun
        fail_mode: secure
        new_option: ignored
        Port "vxlan-aca80118"
            Interface "vxlan-aca80118"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="172.168.1.26", out_key=flow, remote_ip="172.168.1.24"}
        Port "vxlan-aca80119"
            Interface "vxlan-aca80119"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="172.168.1.26", out_key=flow, remote_ip="172.168.1.25"}
        Port "vxlan-aca80117"
            Interface "vxlan-aca80117"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="172.168.1.26", out_key=flow, remote_ip="172.168.1.23"}
        Port patch-int
            Interface patch-int
                type: patch
                options: {peer=patch-tun}
        Port "vxlan-aca80116"
            Interface "vxlan-aca80116"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="172.168.1.26", out_key=flow, remote_ip="172.168.1.22"}
        Port br-tun
            Interface br-tun
                type: internal
    ovs_version: "2.3.2"
""".strip()

ovs_vsctl_show_missing_lines = """
e4d4f521-086d-4479-a88f-d531cd1646b8
    Bridge br-ex
"""


def test_ovs_vsctl_show():
    ovs_ctl_cls = ovs_vsctl_show.OVSvsctlshow(context_wrap(ovs_vsctl_show_output))
    assert ovs_ctl_cls.get_ovs_version() == "2.3.2"
    assert ovs_ctl_cls.get_bridge("br-int").get("fail_mode") == "secure"
    br_tun = ovs_ctl_cls.get_bridge("br-tun")
    assert br_tun.get("fail_mode") == "secure"
    assert len(br_tun.get("ports")) == 6
    ports = br_tun.get("ports")
    assert ports[0].get("interface") == "vxlan-aca80118"
    assert ports[0].get("type") == "vxlan"
    options = ports[0].get("options")
    assert options.get("df_default") == "true"
    assert options.get("local_ip") == "172.168.1.26"
    assert options.get("out_key") == "flow"

    bad = ovs_vsctl_show.OVSvsctlshow(context_wrap(ovs_vsctl_show_missing_lines))
    assert not hasattr(bad, 'data')
