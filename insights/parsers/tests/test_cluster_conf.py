from insights.parsers import cluster_conf
from insights.tests import context_wrap

CLUSTER_CONF_INFO = """
<cluster name="mycluster" config_version="3">
   <clusternodes>
     <clusternode name="node-01.example.com" nodeid="1">
         <fence>
            <method name="APC">
                <device name="apc" port="1"/>
             </method>
            <method name="SAN">
                <device name="sanswitch1" port="12" action="on"/>
                <device name="sanswitch2" port="12" action="on"/>
            </method>
         </fence>
     </clusternode>
     <clusternode name="node-02.example.com" nodeid="2">
         <fence>
            <method name="APC">
              <device name="apc" port="2"/>
            </method>
            <method name="SAN">
                <device name="sanswitch1" port="12"/>
            </method>
         </fence>
     </clusternode>
    </clusternodes>
    <cman expected_votes="3"/>
    <fencedevices>
        <fencedevice agent="fence_imm" ipaddr="139.223.41.219" login="opmgr" name="fence1" passwd="***"/>
        <fencedevice agent="fence_imm" ipaddr="139.223.41.229" login="opmgr" name="fence2" passwd="***"/>
    </fencedevices>
   <rm>
    <resources>
       <lvm name="lvm" vg_name="shared_vg" lv_name="ha-lv"/>
       <fs name="FS" device="/dev/shared_vg/ha-lv" force_fsck="0" force_unmount="1" fsid="64050" fstype="ext4" mountpoint="/mnt" options="" self_fence="0"/>
    </resources>
   </rm>
</cluster>
"""


def test_cluster_conf():
    context = context_wrap(CLUSTER_CONF_INFO)
    result = cluster_conf.get_cluster_conf(context)
    nodes = result["nodes"]
    assert len(nodes) == 2
    assert nodes[0]["name"] == "node-01.example.com"
    fence = nodes[0]["fences"]
    assert len(fence) == 2
    method = fence[1]
    assert len(method) == 2
    assert method["meth_name"] == "SAN"
    assert len(method["device"]) == 2
    assert method["device"][0] == {"action": "on", "name": "sanswitch1", "port": "12"}
    assert nodes[1]["nodeid"] == "2"

    assert len(result["fencedevices"]) == 2
    assert result["fencedevices"][0] == {"passwd": "***", "login": "opmgr", "ipaddr": "139.223.41.219", "name": "fence1", "agent": "fence_imm"}

    assert result["resources"]["lvm"] == {"name": "lvm", "vg_name": "shared_vg", "lv_name": "ha-lv"}
