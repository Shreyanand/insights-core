"""
This module defines all datasources used by standard Red Hat Insight components.

To define data sources that override the components in this file, create a
`insights.core.spec_factory.SpecFactory` with "insights.specs" as the constructor
argument. Data sources created with that factory will override components in
this file with the same `name` keyword argument. This allows overriding the
data sources that standard Insights `Parsers` resolve against.
"""

import os
import re

from insights.config import format_rpm

from insights.core.context import ClusterArchiveContext
from insights.core.context import DockerHostContext
from insights.core.context import DockerImageContext
from insights.core.context import HostContext
from insights.core.context import HostArchiveContext
from insights.core.context import OpenShiftContext

from insights.core.plugins import datasource
from insights.core.spec_factory import CommandOutputProvider, ContentException
from insights.core.spec_factory import simple_file, simple_command, glob_file
from insights.core.spec_factory import first_of, foreach_collect, foreach_execute
from insights.core.spec_factory import first_file, listdir
from insights.specs import Specs


class ProdSpecs(Specs):
    autofs_conf = simple_file("/etc/autofs.conf")
    audit_log = simple_file("/var/log/audit/audit.log")
    auditd_conf = simple_file("/etc/audit/auditd.conf")
    blkid = simple_command("/sbin/blkid -c /dev/null")
    bond = glob_file("/proc/net/bonding/bond*")
    branch_info = simple_file("/branch_info")
    brctl_show = simple_command("/usr/sbin/brctl show")
    candlepin_log = simple_file("/var/log/candlepin/candlepin.log")
    candlepin_error_log = first_of([
                                   simple_command("/var/log/candlepin/error.log"),
                                   simple_file(r"sos_commands/foreman/foreman-debug/var/log/candlepin/error.log",
                                   context=HostArchiveContext)
                                   ])
    ps_auxww = first_of([
                        simple_command("/bin/ps auxww"),
                        simple_file('sos_commands/process/ps_aux', context=HostArchiveContext),
                        simple_file('sos_commands/process/ps_auxwww', context=HostArchiveContext),
                        simple_file('sos_commands/process/ps_auxcww', context=HostArchiveContext),
                        ])

    @datasource(ps_auxww)
    def tomcat_base(broker):
        ps = broker[ProdSpecs.ps_auxww].content
        results = []
        findall = re.compile(r"\-Dcatalina\.base=(\S+)").findall
        for p in ps:
            found = findall(p)
            if found:
                # Only get the path which is absolute
                results.extend(f for f in found if f[0] == '/')
        return list(set(results))

    catalina_out = first_of([
                            foreach_collect(tomcat_base, "%s/catalina.out"),
                            glob_file("tomcat-logs/tomcat*/catalina.out", context=HostArchiveContext)
                            ])
    catalina_server_log = first_of([
                                   foreach_collect(tomcat_base, "%s/catalina*.log"),
                                   glob_file("tomcat-logs/tomcat*/catalina*.log", context=HostArchiveContext)
                                   ])
    cciss = glob_file("/proc/driver/cciss/cciss*")
    ceilometer_central_log = simple_file("/var/log/ceilometer/central.log")
    ceilometer_collector_log = simple_file("/var/log/ceilometer/collector.log")
    ceilometer_conf = simple_file("/etc/ceilometer/ceilometer.conf")
    ceph_socket_files = listdir("/var/run/ceph/ceph-*.*.asok", context=HostContext)
    ceph_config_show = foreach_execute(ceph_socket_files, "/usr/bin/ceph daemon %s config show")
    ceph_df_detail = simple_command("/usr/bin/ceph df detail -f json-pretty")
    ceph_health_detail = simple_command("/usr/bin/ceph health detail -f json-pretty")
    ceph_osd_dump = simple_command("/usr/bin/ceph osd dump -f json-pretty")
    ceph_osd_df = simple_command("/usr/bin/ceph osd df -f json-pretty")
    ceph_osd_ec_profile_ls = simple_command("/usr/bin/ceph osd erasure-code-profile ls")
    ceph_osd_ec_profile_get = foreach_execute(ceph_osd_ec_profile_ls, "/usr/bin/ceph osd erasure-code-profile get %s -f json-pretty")
    ceph_osd_log = glob_file(r"var/log/ceph/ceph-osd*.log")
    ceph_osd_tree = simple_command("/usr/bin/ceph osd tree -f json-pretty")
    ceph_s = simple_command("/usr/bin/ceph -s -f json-pretty")
    ceph_v = simple_command("/usr/bin/ceph -v")
    certificates_enddate = simple_command("/usr/bin/find /etc/origin/node /etc/origin/master /etc/pki -type f -exec /usr/bin/openssl x509 -noout -enddate -in '{}' \; -exec echo 'FileName= {}' \;")
    chkconfig = simple_command("/sbin/chkconfig --list")
    chrony_conf = simple_file("/etc/chrony.conf")
    chronyc_sources = simple_command("/usr/bin/chronyc sources")
    cib_xml = simple_file("/var/lib/pacemaker/cib/cib.xml")
    cinder_conf = simple_file("/etc/cinder/cinder.conf")
    cinder_volume_log = simple_file("/var/log/cinder/volume.log")
    cluster_conf = simple_file("/etc/cluster/cluster.conf")
    cmdline = simple_file("/proc/cmdline")
    cpe = simple_file("/etc/system-release-cpe")
    cobbler_settings = first_file(["/etc/cobbler/settings", "/conf/cobbler/settings"])
    cobbler_modules_conf = first_file(["/etc/cobbler/modules.conf", "/conf/cobbler/modules.conf"])
    corosync = simple_file("/etc/sysconfig/corosync")
    cpuinfo = first_file(["/proc/cpuinfo", "/cpuinfo"])
    cpuinfo_max_freq = simple_file("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")
    current_clocksource = simple_file("/sys/devices/system/clocksource/clocksource0/current_clocksource")
    date = simple_command("/bin/date")
    date_iso = simple_command("/bin/date --iso-8601=seconds")
    date_utc = simple_command("/bin/date --utc")
    df__al = simple_command("/bin/df -al")
    df__alP = simple_command("/bin/df -alP")
    df__li = simple_command("/bin/df -li")
    dig = simple_command("/usr/bin/dig +dnssec . DNSKEY")
    dig_dnssec = simple_command("/usr/bin/dig +dnssec . SOA")
    dig_edns = simple_command("/usr/bin/dig +edns=0 . SOA")
    dig_noedns = simple_command("/usr/bin/dig +noedns . SOA")
    dirsrv = simple_file("/etc/sysconfig/dirsrv")
    dirsrv_access = glob_file("var/log/dirsrv/*/access")
    dirsrv_errors = glob_file("var/log/dirsrv/*/errors")
    display_java = simple_command("/usr/sbin/alternatives --display java")
    dmesg = simple_command("/bin/dmesg")
    dmidecode = simple_command("/usr/sbin/dmidecode")
    docker_info = simple_command("/usr/bin/docker info")
    docker_list_containers = simple_command("/usr/bin/docker ps --all --no-trunc")
    docker_list_images = simple_command("/usr/bin/docker images --all --no-trunc --digests")

    @datasource(docker_list_images)
    def docker_image_ids(broker):
        images = broker[ProdSpecs.docker_list_images]
        try:
            result = set()
            for l in images.content[1:]:
                result.add(l.split(None)[3].strip())
        except:
            raise ContentException("No docker images.")
        if result:
            return list(result)
        raise ContentException("No docker images.")

    # TODO: This parsing is broken.
    @datasource(docker_list_containers)
    def docker_container_ids(broker):
        containers = broker[ProdSpecs.docker_list_containers]
        try:
            result = set()
            for l in containers.content[1:]:
                result.add(l.split(None)[3].strip())
        except:
            raise ContentException("No docker containers.")
        if result:
            return list(result)
        raise ContentException("No docker containers.")

    docker_host_machine_id = simple_file("/etc/redhat-access-insights/machine-id", context=DockerHostContext)
    docker_image_inspect = foreach_execute(docker_image_ids, "/usr/bin/docker inspect %s", context=DockerHostContext)
    docker_container_inspect = foreach_execute(docker_container_ids, "/usr/bin/docker inspect %s", context=DockerHostContext)
    docker_network = simple_file("/etc/sysconfig/docker-network", context=DockerHostContext)
    docker_storage = simple_file("/etc/sysconfig/docker-storage", context=DockerHostContext)
    docker_storage_setup = simple_file("/etc/sysconfig/docker-storage-setup", context=DockerHostContext)
    docker_sysconfig = simple_file("/etc/sysconfig/docker", context=DockerHostContext)
    dumpdev = simple_command("/bin/awk '/ext[234]/ { print $1; }' /proc/mounts")
    dumpe2fs_h = foreach_execute(dumpdev, "/sbin/dumpe2fs -h %s")
    engine_log = simple_file("/var/log/ovirt-engine/engine.log")

    etc_journald_conf = simple_file(r"etc/systemd/journald.conf")
    etc_journald_conf_d = glob_file(r"etc/systemd/journald.conf.d/*.conf")
    ethernet_interfaces = listdir("/sys/class/net", context=HostContext)
    dcbtool_gc_dcb = foreach_execute(ethernet_interfaces, "/sbin/dcbtool gc %s dcb")
    ethtool = foreach_execute(ethernet_interfaces, "/sbin/ethtool %s")
    ethtool_S = foreach_execute(ethernet_interfaces, "/sbin/ethtool -S %s")
    ethtool_a = foreach_execute(ethernet_interfaces, "/sbin/ethtool -a %s")
    ethtool_c = foreach_execute(ethernet_interfaces, "/sbin/ethtool -c %s")
    ethtool_g = foreach_execute(ethernet_interfaces, "/sbin/ethtool -g %s")
    ethtool_i = foreach_execute(ethernet_interfaces, "/sbin/ethtool -i %s")
    ethtool_k = foreach_execute(ethernet_interfaces, "/sbin/ethtool -k %s")
    exim_conf = simple_file("etc/exim.conf")
    facter = simple_command("/usr/bin/facter")
    fc_match = simple_command("/bin/fc-match -sv 'sans:regular:roman' family fontformat")
    fdisk_l = simple_command("/sbin/fdisk -l")
    fdisk_l_sos = glob_file(r"sos_commands/filesys/fdisk_-l_*", context=HostArchiveContext)
    foreman_production_log = simple_file("/var/log/foreman/production.log")
    foreman_proxy_conf = simple_file("/etc/foreman-proxy/settings.yml")
    foreman_proxy_log = simple_file("/var/log/foreman-proxy/proxy.log")
    foreman_satellite_log = simple_file("/var/log/foreman-installer/satellite.log")
    foreman_ssl_access_ssl_log = first_of([simple_file("var/log/httpd/foreman-ssl_access_ssl.log"), simple_file(r"sos_commands/foreman/foreman-debug/var/log/httpd/foreman-ssl_access_ssl.log", context=HostArchiveContext)])
    fstab = simple_file("/etc/fstab")
    galera_cnf = simple_file("/etc/my.cnf.d/galera.cnf")
    getcert_list = first_of([simple_command("/usr/bin/getcert list"), simple_file("sos_commands/ipa/ipa-getcert_list", context=HostArchiveContext)])
    getenforce = simple_command("/usr/sbin/getenforce")
    getsebool = simple_command("/usr/sbin/getsebool -a")
    glance_api_conf = simple_file("/etc/glance/glance-api.conf")
    glance_api_log = simple_file("/var/log/glance/api.log")
    glance_cache_conf = simple_file("/etc/glance/glance-cache.conf")
    glance_registry_conf = simple_file("/etc/glance/glance-registry.conf")
    grub_conf = simple_file("/boot/grub/grub.conf")
    grub_efi_conf = simple_file("/boot/efi/EFI/redhat/grub.conf")
    grub2_cfg = simple_file("/boot/grub2/grub.cfg")
    grub2_efi_cfg = simple_file("boot/efi/EFI/redhat/grub.cfg")
    grub_config_perms = simple_command("/bin/ls -l /boot/grub2/grub.cfg")  # only RHEL7 and updwards
    grub1_config_perms = simple_command("/bin/ls -l /boot/grub/grub.conf")  # RHEL6
    hammer_ping = simple_command("/usr/bin/hammer ping")
    haproxy_cfg = simple_file("/etc/haproxy/haproxy.cfg")
    heat_api_log = simple_file("/var/log/heat/heat-api.log")
    heat_conf = simple_file("/etc/heat/heat.conf")
    heat_crontab = simple_command("/usr/bin/crontab -l -u heat")
    heat_engine_log = simple_file("/var/log/heat/heat-engine.log")
    hostname = simple_command("/usr/bin/hostname -f")
    hosts = simple_file("/etc/hosts")
    hponcfg_g = simple_command("/sbin/hponcfg -g")
    httpd_access_log = simple_file("/var/log/httpd/access_log")
    httpd_conf = glob_file(["/etc/httpd/conf/httpd.conf", "/etc/httpd/conf.d/*.conf"]),
    httpd_conf_sos = glob_file(["/conf/httpd/conf/httpd.conf", "/conf/httpd/conf.d/*.conf"], context=HostArchiveContext)
    httpd_error_log = simple_file("var/log/httpd/error_log")
    httpd_pid = simple_command("/bin/ps aux | grep /usr/sbin/httpd | grep -v grep | head -1 | awk '{print $2}'")
    httpd_limits = foreach_collect(httpd_pid, "/proc/%s/limits")
    httpd_ssl_access_log = simple_file("/var/log/httpd/ssl_access_log")
    httpd_ssl_error_log = simple_file("/var/log/httpd/ssl_error_log")

    @datasource(ps_auxww)
    def httpd_cmd(broker):
        ps = broker[ProdSpecs.ps_auxww].content
        for p in ps:
            p_splits = p.split(None, 10)
            if len(p_splits) >= 11:
                cmd = p_splits[10].split()[0]
                # Should compatible with RHEL6
                # e.g. /usr/sbin/httpd, /usr/sbin/httpd.worker and /usr/sbin/httpd.event
                if 'httpd' in os.path.basename(cmd):
                    return [cmd]
        return []

    httpd_V = foreach_execute(httpd_cmd, "%s -V")
    ifcfg = glob_file("/etc/sysconfig/network-scripts/ifcfg-*")
    ifconfig = simple_command("/sbin/ifconfig -a")
    imagemagick_policy = glob_file(["/etc/ImageMagick/policy.xml", "/usr/lib*/ImageMagick-6.5.4/config/policy.xml"])
    init_ora = simple_file("${ORACLE_HOME}/dbs/init.ora")
    initscript = glob_file(r"etc/rc.d/init.d/*")
    interrupts = simple_file("/proc/interrupts")
    ip_addr = simple_command("/sbin/ip addr")
    ip_route_show_table_all = simple_command("/sbin/ip route show table all")
    ip_s_link = simple_command("/sbin/ip -s link")
    ipaupgrade_log = simple_file("/var/log/ipaupgrade.log")
    ipcs_s = simple_command("/usr/bin/ipcs -s")
    semid = simple_command("/usr/bin/ipcs -s | awk '{if (NF == 5 && $NF ~ /^[0-9]+$/) print $NF}'")
    ipcs_s_i = foreach_execute(semid, "/usr/bin/ipcs -s -i %s")
    iptables = simple_command("/sbin/iptables-save")
    iptables_permanent = simple_file("etc/sysconfig/iptables")
    ip6tables = simple_command("/sbin/ip6tables-save")
    ip6tables_permanent = simple_file("etc/sysconfig/ip6tables")
    ipv4_neigh = simple_command("/sbin/ip -4 neighbor show nud all")
    ipv6_neigh = simple_command("/sbin/ip -6 neighbor show nud all")
    iscsiadm_m_session = simple_command("/usr/sbin/iscsiadm -m session")
    journal_since_boot = simple_file("sos_commands/logs/journalctl_--no-pager_--boot", context=HostArchiveContext)
    katello_service_status = simple_command("/usr/bin/katello-service status")
    kdump = simple_file("/etc/sysconfig/kdump")
    kdump_conf = simple_file("/etc/kdump.conf")
    kerberos_kdc_log = simple_file("var/log/krb5kdc.log")
    kexec_crash_loaded = simple_file("/sys/kernel/kexec_crash_loaded")
    kexec_crash_size = simple_file("/sys/kernel/kexec_crash_size")
    keystone_conf = simple_file("/etc/keystone/keystone.conf")
    keystone_crontab = simple_command("/usr/bin/crontab -l -u keystone")
    keystone_log = simple_file("/var/log/keystone/keystone.log")
    krb5 = glob_file([r"etc/krb5.conf", r"etc/krb5.conf.d/*.conf"])
    ksmstate = simple_file("/sys/kernel/mm/ksm/run")
    last_upload_globs = ["/etc/redhat-access-insights/.lastupload", "/etc/insights-client/.lastupload"]
    lastupload = glob_file(last_upload_globs)
    libkeyutils = simple_command("/usr/bin/find -L /lib /lib64 -name 'libkeyutils.so*'")
    libkeyutils_objdumps = simple_command('/usr/bin/find -L /lib /lib64 -name libkeyutils.so.1 -exec objdump -x "{}" \;')
    libvirtd_log = simple_file("/var/log/libvirt/libvirtd.log")
    limits_conf = glob_file(["/etc/security/limits.conf", "/etc/security/limits.d/*.conf"])
    locale = simple_command("/usr/bin/locale")
    localtime = simple_command("/usr/bin/file -L /etc/localtime")
    lpstat_p = simple_command("/usr/bin/lpstat -p")
    lsblk = simple_command("/bin/lsblk")
    lsblk_pairs = simple_command("/bin/lsblk -P -o NAME,KNAME,MAJ:MIN,FSTYPE,MOUNTPOINT,LABEL,UUID,RA,RO,RM,MODEL,SIZE,STATE,OWNER,GROUP,MODE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,TYPE,DISC-ALN,DISC-GRAN,DISC-MAX,DISC-ZERO")
    lscpu = simple_command("/usr/bin/lscpu")
    lsinitrd_lvm_conf = first_of([
                                 simple_command("/sbin/lsinitrd -f /etc/lvm/lvm.conf"),
                                 simple_command("/usr/bin/lsinitrd -f /etc/lvm/lvm.conf")
                                 ])
    lsmod = simple_command("/sbin/lsmod")
    lspci = simple_command("/sbin/lspci")
    lsof = simple_command("/usr/sbin/lsof")
    lssap = simple_command("/usr/sap/hostctrl/exe/lssap")
    ls_boot = simple_command("/bin/ls -lanR /boot")
    ls_docker_volumes = simple_command("/bin/ls -lanR /var/lib/docker/volumes")
    ls_dev = simple_command("/bin/ls -lanR /dev")
    ls_disk = simple_command("/bin/ls -lanR /dev/disk/by-*")
    ls_etc = simple_command("/bin/ls -lanR /etc")
    ls_sys_firmware = simple_command("/bin/ls -lanR /sys/firmware")
    ls_var_log = simple_command("/bin/ls -la /var/log /var/log/audit")
    ls_var_www = simple_command("/bin/ls -la /dev/null /var/www")  # https://github.com/RedHatInsights/insights-core/issues/827
    lvdisplay = simple_command("/sbin/lvdisplay")
    lvm_conf = simple_file("/etc/lvm/lvm.conf")
    lvs = None  # simple_command('/sbin/lvs -a -o +lv_tags,devices --config="global{locking_type=0}"')
    lvs_noheadings = simple_command("/sbin/lvs --nameprefixes --noheadings --separator='|' -a -o lv_name,vg_name,lv_size,region_size,mirror_log,lv_attr,devices,region_size --config=\"global{locking_type=0}\"")
    machine_id = simple_file("etc/redhat-access-insights/machine-id")
    manila_conf = simple_file("/etc/manila/manila.conf")
    mariadb_log = simple_file("/var/log/mariadb/mariadb.log")
    mdstat = simple_file("/proc/mdstat")
    meminfo = first_file(["/proc/meminfo", "/meminfo"])
    messages = simple_file("/var/log/messages")
    metadata_json = simple_file("metadata.json", context=ClusterArchiveContext)
    mlx4_port = simple_command("/usr/bin/find /sys/bus/pci/devices/*/mlx4_port[0-9] -print -exec cat {} \;")
    module = listdir("/sys/module")
    modinfo = foreach_execute(module, "/usr/sbin/modinfo %s")
    modprobe_conf = simple_file("/etc/modprobe.conf")
    sysconfig_mongod = glob_file([
                                 "etc/sysconfig/mongod",
                                 "etc/opt/rh/rh-mongodb26/sysconfig/mongod"
                                 ])
    mongod_conf = glob_file([
                            "/etc/mongod.conf",
                            "/etc/mongodb.conf",
                            "/etc/opt/rh/rh-mongodb26/mongod.conf"
                            ])
    modprobe_d = glob_file("/etc/modprobe.d/*.conf")
    mount = simple_command("/bin/mount")
    multicast_querier = simple_command("/usr/bin/find /sys/devices/virtual/net/ -name multicast_querier -print -exec cat {} \;")
    multipath_conf = simple_file("/etc/multipath.conf")
    multipath__v4__ll = simple_command("/sbin/multipath -v4 -ll")
    named_checkconf_p = simple_command("/usr/sbin/named-checkconf -p")
    netconsole = simple_file("/etc/sysconfig/netconsole")
    netstat = simple_command("/bin/netstat -neopa")
    netstat_agn = simple_command("/bin/netstat -agn")
    netstat_i = simple_command("/bin/netstat -i")
    netstat_s = simple_command("/bin/netstat -s")
    neutron_conf = simple_file("/etc/neutron/neutron.conf")
    neutron_ovs_agent_log = simple_file("/var/log/neutron/openvswitch-agent.log")
    neutron_plugin_ini = simple_file("/etc/neutron/plugin.ini")
    neutron_server_log = simple_file("/var/log/neutron/server.log")
    nfnetlink_queue = simple_file("/proc/net/netfilter/nfnetlink_queue")
    nfs_exports = simple_file("/etc/exports")
    nfs_exports_d = glob_file("/etc/exports.d/*.exports")
    nginx_conf = glob_file([
                           "/etc/nginx/nginx.conf",
                           "/opt/rh/nginx*/root/etc/nginx/nginx.conf",
                           "/etc/opt/rh/rh-nginx*/nginx/nginx.conf"
                           ])
    nova_api_log = simple_file("/var/log/nova/nova-api.log")
    nova_compute_log = simple_file("/var/log/nova/nova-compute.log")
    nova_conf = simple_file("/etc/nova/nova.conf")
    nova_crontab = simple_command("/usr/bin/crontab -l -u nova")
    nscd_conf = simple_file("/etc/nscd.conf")
    nsswitch_conf = simple_file("/etc/nsswitch.conf")
    ntp_conf = simple_file("/etc/ntp.conf")
    ntpq_leap = simple_command("/usr/sbin/ntpq -c 'rv 0 leap'")
    ntpq_pn = simple_command("/usr/sbin/ntpq -pn")
    ntptime = simple_command("/usr/sbin/ntptime")
    numeric_user_group_name = simple_command("/bin/grep -c '^[[:digit:]]' /etc/passwd /etc/group")
    oc_get_pod = simple_command("/usr/bin/oc get pod -o yaml --all-namespaces", context=OpenShiftContext)
    oc_get_bc = simple_command("/usr/bin/oc get bc -o yaml --all-namespaces", context=OpenShiftContext)
    oc_get_dc = simple_command("/usr/bin/oc get dc -o yaml --all-namespaces", context=OpenShiftContext)
    oc_get_endpoints = simple_command("/usr/bin/oc get endpoints -o yaml --all-namespaces", context=OpenShiftContext)
    oc_get_service = simple_command("/usr/bin/oc get service -o yaml --all-namespaces", context=OpenShiftContext)
    oc_get_rolebinding = simple_command("/usr/bin/oc get rolebinding -o yaml --all-namespaces", context=OpenShiftContext)
    oc_get_project = simple_command("/usr/bin/oc get project -o yaml --all-namespaces", context=OpenShiftContext)
    oc_get_role = simple_command("/usr/bin/oc get role -o yaml --all-namespaces", context=OpenShiftContext)
    oc_get_pv = simple_command("/usr/bin/oc get pv -o yaml --all-namespaces", context=OpenShiftContext)
    oc_get_pvc = simple_command("/usr/bin/oc get pvc -o yaml --all-namespaces", context=OpenShiftContext)
    crt = simple_command("/usr/bin/find /etc/origin/node /etc/origin/master -type f -path '*.crt'")
    openshift_certificates = foreach_execute(crt, "/usr/bin/openssl x509 -noout -enddate -in %s")
    openvswitch_server_log = simple_file('/var/log/openvswitch/ovsdb-server.log')
    openvswitch_daemon_log = simple_file('/var/log/openvswitch/ovs-vswitchd.log')
    os_release = simple_file("etc/os-release")
    osa_dispatcher_log = first_file([
                                    "/var/log/rhn/osa-dispatcher.log",
                                    "/rhn-logs/rhn/osa-dispatcher.log"
                                    ])
    ose_master_config = simple_file("/etc/origin/master/master-config.yaml")
    ose_node_config = simple_file("/etc/origin/node/node-config.yaml")
    ovirt_engine_confd = glob_file("/etc/ovirt-engine/engine.conf.d/*")
    ovirt_engine_server_log = simple_file("/var/log/ovirt-engine/server.log")
    ovs_vsctl_show = simple_command("/usr/bin/ovs-vsctl show")
    pacemaker_log = simple_file("/var/log/pacemaker.log")
    running_java = simple_command("/bin/ps auxwww | grep java | grep -v grep| awk '{print $11}' | sort -u")
    package_provides_java = foreach_execute(running_java, "echo %s $(readlink -e `which %s` | xargs rpm -qf)")
    pam_conf = simple_file("/etc/pam.conf")
    parted__l = simple_command("/sbin/parted -l -s")
    password_auth = simple_file("/etc/pam.d/password-auth")
    pcs_status = simple_command("/usr/sbin/pcs status")
    pluginconf_d = glob_file("/etc/yum/pluginconf.d/*.conf")
    postgresql_conf = first_file([
                                 "/var/lib/pgsql/data/postgresql.conf",
                                 "/opt/rh/postgresql92/root/var/lib/pgsql/data/postgresql.conf",
                                 "database/postgresql.conf"
                                 ])
    postgresql_log = first_of([
                              glob_file("/var/lib/pgsql/data/pg_log/postgresql-*.log"),
                              glob_file("/opt/rh/postgresql92/root/var/lib/pgsql/data/pg_log/postgresql-*.log"),
                              glob_file("/database/postgresql-*.log")
                              ])
    md5chk_files = simple_command("/bin/ls -H /usr/lib*/{libfreeblpriv3.so,libsoftokn3.so} /etc/pki/product*/69.pem /etc/fonts/fonts.conf /dev/null 2>/dev/null")
    prelink_orig_md5 = None
    prev_uploader_log = simple_file("var/log/redhat-access-insights/redhat-access-insights.log.1")
    puppet_ssl_cert_ca_pem = None
    pvs = simple_command('/sbin/pvs -a -v -o +pv_mda_free,pv_mda_size,pv_mda_count,pv_mda_used_count,pe_count --config="global{locking_type=0}"')
    pvs_noheadings = simple_command("/sbin/pvs --nameprefixes --noheadings --separator='|' -a -o pv_all,vg_name --config=\"global{locking_type=0}\"")
    qemu_conf = simple_file("/etc/libvirt/qemu.conf")
    qpid_stat_q = simple_command("/usr/bin/qpid-stat -q --ssl-certificate=/etc/pki/katello/qpid_client_striped.crt -b amqps://localhost:5671")
    qpid_stat_u = simple_command("/usr/bin/qpid-stat -u --ssl-certificate=/etc/pki/katello/qpid_client_striped.crt -b amqps://localhost:5671")
    rabbitmq_logs = glob_file("/var/log/rabbitmq/rabbit@*.log", ignore=".*rabbit@.*(?<!-sasl).log$")
    rabbitmq_policies = simple_command("/usr/sbin/rabbitmqctl list_policies")
    rabbitmq_queues = simple_command("/usr/sbin/rabbitmqctl list_queues name messages consumers auto_delete")
    rabbitmq_report = simple_command("/usr/sbin/rabbitmqctl report")
    rabbitmq_startup_err = simple_file("/var/log/rabbitmq/startup_err")
    rabbitmq_startup_log = simple_file("/var/log/rabbitmq/startup_log")
    rabbitmq_users = simple_command("/usr/sbin/rabbitmqctl list_users")
    rc_local = simple_file("/etc/rc.d/rc.local")
    redhat_release = simple_file("/etc/redhat-release")
    resolv_conf = simple_file("/etc/resolv.conf")
    rhn_charsets = simple_command("/usr/bin/rhn-charsets")
    rhn_conf = first_file(["/etc/rhn/rhn.conf", "/conf/rhn/rhn/rhn.conf"])
    rhn_entitlement_cert_xml = first_of([glob_file("/etc/sysconfig/rhn/rhn-entitlement-cert.xml*"),
                                   glob_file("/conf/rhn/sysconfig/rhn/rhn-entitlement-cert.xml*")])
    rhn_hibernate_conf = first_file(["/usr/share/rhn/config-defaults/rhn_hibernate.conf", "/config-defaults/rhn_hibernate.conf"])
    rhn_schema_stats = simple_command("/usr/bin/rhn-schema-stats -")
    rhn_schema_version = simple_command("/usr/bin/rhn-schema-version")
    rhn_server_satellite_log = simple_file("var/log/rhn/rhn_server_satellite.log")
    rhn_server_xmlrpc_log = first_file(["/var/log/rhn/rhn_server_xmlrpc.log",
                                           "/rhn-logs/rhn/rhn_server_xmlrpc.log"])
    rhn_search_daemon_log = first_file(["/var/log/rhn/search/rhn_search_daemon.log",
                                           "/rhn-logs/rhn/search/rhn_search_daemon.log"])
    rhn_taskomatic_daemon_log = first_file(["/var/log/rhn/rhn_taskomatic_daemon.log",
                                               "rhn-logs/rhn/rhn_taskomatic_daemon.log"])
    rhsm_conf = simple_file("/etc/rhsm/rhsm.conf")
    rhsm_log = simple_file("/var/log/rhsm/rhsm.log")
    root_crontab = simple_command("/usr/bin/crontab -l -u root")
    route = simple_command("/sbin/route -n")
    rpm_V_packages = simple_command("/usr/bin/rpm -V coreutils procps procps-ng shadow-utils passwd sudo")
    rsyslog_conf = simple_file("/etc/rsyslog.conf")
    samba = simple_file("/etc/samba/smb.conf")
    satellite_version_rb = simple_file("/usr/share/foreman/lib/satellite/version.rb")
    block_devices = listdir("/sys/block")
    scheduler = foreach_collect(block_devices, "/sys/block/%s/queue/scheduler")
    scsi = simple_file("/proc/scsi/scsi")
    secure = simple_file("/var/log/secure")
    selinux_config = simple_file("/etc/selinux/config")
    sestatus = simple_command("/usr/sbin/sestatus -b")

    @datasource(HostContext)
    def block(broker):
        remove = (".", "ram", "dm-", "loop")
        tmp = "/dev/%s"
        return[(tmp % f) for f in os.listdir("/sys/block") if not f.startswith(remove)]

    smbstatus_p = simple_command("/usr/bin/smbstatus -p")
    smbstatus_S = simple_command("/usr/bin/smbstatus -S")
    smartctl = foreach_execute(block, "/sbin/smartctl -a %s", keep_rc=True)
    softnet_stat = simple_file("proc/net/softnet_stat")
    spfile_ora = glob_file("${ORACLE_HOME}/dbs/spfile*.ora")
    ss = simple_command("/usr/sbin/ss -tulpn")
    ssh_config = simple_file("/etc/ssh/ssh_config")
    sshd_config = simple_file("/etc/ssh/sshd_config")
    sshd_config_perms = simple_command("/bin/ls -l /etc/ssh/sshd_config")
    sssd_config = simple_file("/etc/sssd/sssd.conf")
    sssd_logs = glob_file("/var/log/sssd/*.log")
    swift_object_expirer_conf = simple_file("etc/swift/object-expirer.conf")
    swift_proxy_server_conf = simple_file("etc/swift/proxy-server.conf")
    sysconfig_chronyd = simple_file("/etc/sysconfig/chronyd")
    sysconfig_httpd = simple_file("/etc/sysconfig/httpd")
    sysconfig_irqbalance = simple_file("etc/sysconfig/irqbalance")
    sysconfig_kdump = simple_file("etc/sysconfig/kdump")
    sysconfig_ntpd = simple_file("/etc/sysconfig/ntpd")
    sysconfig_virt_who = simple_file("/etc/sysconfig/virt-who")
    sysctl = simple_command("/sbin/sysctl -a")
    sysctl_conf = simple_file("/etc/sysctl.conf")
    sysctl_conf_initramfs = simple_command("/bin/lsinitrd /boot/initramfs-*kdump.img -f /etc/sysctl.conf /etc/sysctl.d/*.conf")
    systemctl_cinder_volume = simple_command("/bin/systemctl show openstack-cinder-volume")
    systemctl_list_unit_files = simple_command("/bin/systemctl list-unit-files")
    systemctl_list_units = simple_command("/bin/systemctl list-units")
    systemctl_mariadb = simple_command("/bin/systemctl show mariadb")
    systemd_docker = simple_file("/usr/lib/systemd/system/docker.service")
    systemd_openshift_node = simple_file("/usr/lib/systemd/system/atomic-openshift-node.service")
    systemd_system_conf = simple_file("/etc/systemd/system.conf")
    systemid = first_of([
        simple_file("/etc/sysconfig/rhn/systemid"),
        simple_file("/conf/rhn/sysconfig/rhn/systemid")
    ])
    teamdctl_state_dump = foreach_execute(ethernet_interfaces, "/usr/bin/teamdctl %s state dump")
    thp_use_zero_page = simple_file("/sys/kernel/mm/transparent_hugepage/use_zero_page")
    thp_enabled = simple_file("/sys/kernel/mm/transparent_hugepage/enabled")
    tmpfilesd = glob_file(["/etc/tmpfiles.d/*.conf", "/usr/lib/tmpfiles.d/*.conf", "/run/tmpfiles.d/*.conf"])
    tomcat_web_xml = first_of([glob_file("/etc/tomcat*/web.xml"),
                                  glob_file("/conf/tomcat/tomcat*/web.xml")])

    @datasource(ps_auxww)
    def tomcat_home_base(broker):
        ps = broker[ProdSpecs.ps_auxww].content
        results = []
        findall = re.compile(r"\-Dcatalina\.(home|base)=(\S+)").findall
        for p in ps:
            found = findall(p)
            if found:
                # Only get the path which is absolute
                results.extend(f[1] for f in found if f[1][0] == '/')
        return list(set(results))

    tomcat_vdc_targeted = foreach_execute(tomcat_home_base, "/bin/grep -R -s 'VirtualDirContext' --include '*.xml' %s")
    tomcat_vdc_fallback = simple_command("/usr/bin/find /usr/share -maxdepth 1 -name 'tomcat*' -exec /bin/grep -R -s 'VirtualDirContext' --include '*.xml' '{}' +")
    tuned_adm = simple_command("/usr/sbin/tuned-adm list")
    udev_persistent_net_rules = simple_file("/etc/udev/rules.d/70-persistent-net.rules")
    uname = simple_command("/usr/bin/uname -a")
    up2date = simple_file("/etc/sysconfig/rhn/up2date")
    uploader_log = simple_file("/var/log/redhat-access-insights/redhat-access-insights.log")
    uptime = simple_command("/usr/bin/uptime")
    usr_journald_conf_d = glob_file(r"usr/lib/systemd/journald.conf.d/*.conf")  # note that etc_journald.conf.d also exists
    vgdisplay = simple_command("/sbin/vgdisplay")
    vdsm_conf = simple_file("etc/vdsm/vdsm.conf")
    vdsm_id = simple_file("etc/vdsm/vdsm.id")
    vdsm_log = simple_file("var/log/vdsm/vdsm.log")
    vgs = None  # simple_command('/sbin/vgs -v -o +vg_mda_count,vg_mda_free,vg_mda_size,vg_mda_used_count,vg_tags --config="global{locking_type=0}"')
    vgs_noheadings = simple_command("/sbin/vgs --nameprefixes --noheadings --separator='|' -a -o vg_all --config=\"global{locking_type=0}\"")
    virt_what = simple_command("/usr/sbin/virt-what")
    virt_who_conf = glob_file([r"etc/virt-who.conf", r"etc/virt-who.d/*.conf"])
    vmcore_dmesg = glob_file("/var/crash/*/vmcore-dmesg.txt")
    vsftpd = simple_file("/etc/pam.d/vsftpd")
    vsftpd_conf = simple_file("/etc/vsftpd/vsftpd.conf")
    woopsie = simple_command(r"/usr/bin/find /var/crash /var/tmp -path '*.reports-*/whoopsie-report'")
    xfs_info = None
    xinetd_conf = glob_file(["/etc/xinetd.conf", "/etc/xinetd.d/*"])
    yum_conf = simple_file("/etc/yum.conf")
    yum_log = simple_file("/var/log/yum.log")
    yum_repolist = simple_command("/usr/bin/yum -C repolist")
    yum_repos_d = glob_file("/etc/yum.repos.d/*")

    rpm_format = format_rpm()

    host_installed_rpms = simple_command("/usr/bin/rpm -qa --qf '%s'" % rpm_format, context=HostContext)

    @datasource(DockerImageContext)
    def docker_installed_rpms(broker):
        ctx = broker[DockerImageContext]
        root = ctx.root
        fmt = ProdSpecs.rpm_format
        cmd = "/usr/bin/rpm -qa --root %s --qf '%s'" % (root, fmt)
        result = ctx.shell_out(cmd)
        return CommandOutputProvider(cmd, ctx, content=result)

    # unify the different installed rpm provider types
    installed_rpms = first_of([host_installed_rpms, docker_installed_rpms])

    @datasource(ps_auxww)
    def jboss_domain_server_log_dir(broker):
        ps = broker[ProdSpecs.ps_auxww].content
        results = []
        findall = re.compile(r"\-Djboss\.server\.log\.dir=(\S+)").findall
        # JBoss domain server progress command content should contain jboss.server.log.dir
        for p in ps:
            if '-D[Server:' in p:
                found = findall(p)
                if found:
                    # Only get the path which is absolute
                    results.extend(f for f in found if f[0] == '/')
        return list(set(results))

    jboss_domain_server_log = foreach_collect(jboss_domain_server_log_dir, "%s/server.log*")
