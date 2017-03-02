from falafel.mappers.neutron_ovs_agent_log import NeutronOVSAgentLog
from falafel.tests import context_wrap


LOG = """
2016-11-09 14:39:25.348 3153 WARNING oslo_config.cfg [-] Option "rabbit_password" from group "oslo_messaging_rabbit" is deprecated for removal.  Its value may be silently ignored in the future.
2016-11-09 14:39:25.348 3153 WARNING oslo_config.cfg [-] Option "rabbit_userid" from group "oslo_messaging_rabbit" is deprecated for removal.  Its value may be silently ignored in the future.
2016-11-09 14:39:25.352 3153 INFO ryu.base.app_manager [-] loading app neutron.plugins.ml2.drivers.openvswitch.agent.openflow.native.ovs_ryuapp
2016-11-09 14:39:27.171 3153 INFO ryu.base.app_manager [-] loading app ryu.app.ofctl.service
2016-11-09 14:39:27.190 3153 INFO ryu.base.app_manager [-] loading app ryu.controller.ofp_handler
"""


def test_neutron_ovs_agent_log():
    log = NeutronOVSAgentLog(context_wrap(LOG))
    assert len(log.get("WARNING")) == 2
