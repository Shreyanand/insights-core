from falafel.mappers.pcs_status import PCSStatus
from falafel.tests import context_wrap

pcs_0 = """
Cluster name: openstack
Last updated: Fri Oct 14 15:45:32 2016
Last change: Thu Oct 13 20:02:27 2016
Stack: corosync
Current DC: myhost15 (1) - partition with quorum
Version: 1.1.12-a14efad
3 Nodes configured
143 Resources configured


Online: [ myhost15 myhost16 myhost17 ]

Full list of resources:

 stonith-ipmilan-10.24.221.172	(stonith:fence_ipmilan):	Started myhost15
 stonith-ipmilan-10.24.221.171	(stonith:fence_ipmilan):	Started myhost16
 stonith-ipmilan-10.24.221.173	(stonith:fence_ipmilan):	Started myhost15
 ip-ceilometer-pub-10.50.218.121	(ocf::heartbeat:IPaddr2):	Started myhost15
 ip-neutron-pub-10.50.218.129	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-ceilometer-prv-10.24.82.127	(ocf::heartbeat:IPaddr2):	Started myhost15
 ip-ceilometer-adm-10.24.82.126	(ocf::heartbeat:IPaddr2):	Started myhost15
 ip-horizon-pub-10.50.218.126	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-horizon-adm-10.24.82.137	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-amqp-pub-10.24.82.145	(ocf::heartbeat:IPaddr2):	Started myhost15
 ip-loadbalancer-pub-10.50.218.128	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-neutron-adm-10.24.82.141	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-neutron-prv-10.24.82.142	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-horizon-prv-10.24.82.138	(ocf::heartbeat:IPaddr2):	Started myhost16
 Clone Set: memcached-clone [memcached]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: haproxy-clone [haproxy]
     Started: [ myhost15 myhost16 myhost17 ]
 ip-galera-pub-10.24.82.130	(ocf::heartbeat:IPaddr2):	Started myhost15
 Master/Slave Set: galera-master [galera]
     Masters: [ myhost15 myhost16 myhost17 ]
 Clone Set: rabbitmq-server-clone [rabbitmq-server]
     Started: [ myhost15 myhost16 myhost17 ]
 ip-keystone-pub-10.50.218.127	(ocf::heartbeat:IPaddr2):	Started myhost15
 ip-keystone-adm-10.24.82.139	(ocf::heartbeat:IPaddr2):	Started myhost15
 ip-keystone-prv-10.24.82.140	(ocf::heartbeat:IPaddr2):	Started myhost15
 Clone Set: keystone-clone [keystone]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: fs-varlibglanceimages-clone [fs-varlibglanceimages]
     Started: [ myhost15 myhost16 myhost17 ]
 ip-glance-pub-10.50.218.123	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-glance-prv-10.24.82.132	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-glance-adm-10.24.82.131	(ocf::heartbeat:IPaddr2):	Started myhost16
 Clone Set: glance-registry-clone [glance-registry]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: glance-api-clone [glance-api]
     Started: [ myhost15 myhost16 myhost17 ]
 ip-nova-pub-10.50.218.130	(ocf::heartbeat:IPaddr2):	Started myhost15
 ip-nova-adm-10.24.82.143	(ocf::heartbeat:IPaddr2):	Started myhost15
 ip-nova-prv-10.24.82.144	(ocf::heartbeat:IPaddr2):	Started myhost15
 Clone Set: openstack-nova-novncproxy-clone [openstack-nova-novncproxy]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: openstack-nova-consoleauth-clone [openstack-nova-consoleauth]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: openstack-nova-conductor-clone [openstack-nova-conductor]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: openstack-nova-api-clone [openstack-nova-api]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: openstack-nova-scheduler-clone [openstack-nova-scheduler]
     Started: [ myhost15 myhost16 myhost17 ]
 ip-cinder-pub-10.50.218.122	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-cinder-prv-10.24.82.129	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-cinder-adm-10.24.82.128	(ocf::heartbeat:IPaddr2):	Started myhost16
 Clone Set: cinder-api-clone [cinder-api]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: cinder-scheduler-clone [cinder-scheduler]
     Started: [ myhost15 myhost16 myhost17 ]
 cinder-volume	(systemd:openstack-cinder-volume):	Started myhost15
 ip-heat-pub-10.50.218.124	(ocf::heartbeat:IPaddr2):	Started myhost15
 ip-heat-prv-10.24.82.134	(ocf::heartbeat:IPaddr2):	Started myhost15
 ip-heat-adm-10.24.82.133	(ocf::heartbeat:IPaddr2):	Started myhost15
 ip-heat_cfn-pub-10.50.218.125	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-heat_cfn-prv-10.24.82.136	(ocf::heartbeat:IPaddr2):	Started myhost16
 ip-heat_cfn-adm-10.24.82.135	(ocf::heartbeat:IPaddr2):	Started myhost16
 Clone Set: neutron-server-clone [neutron-server]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: neutron-scale-clone [neutron-scale] (unique)
     neutron-scale:0	(ocf::neutron:NeutronScale):	Started myhost17
     neutron-scale:1	(ocf::neutron:NeutronScale):	Started myhost16
     neutron-scale:2	(ocf::neutron:NeutronScale):	Started myhost15
 Clone Set: neutron-ovs-cleanup-clone [neutron-ovs-cleanup]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: neutron-netns-cleanup-clone [neutron-netns-cleanup]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: neutron-openvswitch-agent-clone [neutron-openvswitch-agent]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: neutron-dhcp-agent-clone [neutron-dhcp-agent]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: neutron-l3-agent-clone [neutron-l3-agent]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: neutron-metadata-agent-clone [neutron-metadata-agent]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: heat-api-clone [heat-api]
     Started: [ myhost15 myhost16 myhost17 ]
 Resource Group: heat
     openstack-heat-engine	(systemd:openstack-heat-engine):	Started myhost15
 Clone Set: heat-api-cfn-clone [heat-api-cfn]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: heat-api-cloudwatch-clone [heat-api-cloudwatch]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: horizon-clone [horizon]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: mongod-clone [mongod]
     Started: [ myhost15 myhost16 myhost17 ]
 openstack-ceilometer-central	(systemd:openstack-ceilometer-central):	Started myhost16
 Clone Set: openstack-ceilometer-api-clone [openstack-ceilometer-api]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: openstack-ceilometer-alarm-evaluator-clone [openstack-ceilometer-alarm-evaluator]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: openstack-ceilometer-collector-clone [openstack-ceilometer-collector]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: openstack-ceilometer-notification-clone [openstack-ceilometer-notification]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: openstack-ceilometer-alarm-notifier-clone [openstack-ceilometer-alarm-notifier]
     Started: [ myhost15 myhost16 myhost17 ]
 Clone Set: ceilometer-delay-clone [ceilometer-delay]
     Started: [ myhost15 myhost16 myhost17 ]
 openstack-nova-compute-vc13cl42	(systemd:openstack-nova-compute-vc13cl42):	Started myhost15
 openstack-manila-api	(systemd:openstack-manila-api):	Started myhost16
 openstack-manila-scheduler	(systemd:openstack-manila-scheduler):	Started myhost16
 openstack-manila-share	(systemd:openstack-manila-share):	Started myhost16
 ip-manila-10.50.218.150	(ocf::heartbeat:IPaddr2):	Started myhost16

PCSD Status:
  myhost15: Online
  myhost17: Online
  myhost16: Online

Daemon Status:
  corosync: active/enabled
  pacemaker: active/enabled
  pcsd: active/enabled
""".strip()


def test_pcs_status():
    pcs = PCSStatus(context_wrap(pcs_0))
    assert pcs.nodes == ['myhost15', 'myhost17', 'myhost16']
    assert pcs.get('Stack') == 'corosync'
    assert pcs.get('Cluster name') == 'openstack'
    assert pcs.get('Current DC') == 'myhost15 (1) - partition with quorum'
    assert pcs.get("Nodes configured") == "3"
    assert pcs.get("Resources configured") == "143"
    assert pcs.get("Online") == "[ myhost15 myhost16 myhost17 ]"
