from falafel.mappers.facter import Facter
from falafel.tests import context_wrap

FACTS = """
COMMAND> facter

architecture => x86_64
augeasversion => 1.1.0
bios_release_date => 04/14/2014
bios_vendor => Phoenix Technologies LTD
bios_version => 6.00
blockdevice_fd0_size => 4096
blockdevice_sda_model => Virtual disk
blockdevice_sda_size => 53687091200
blockdevice_sda_vendor => VMware
blockdevice_sdb_model => Virtual disk
blockdevice_sdb_size => 214748364800
blockdevice_sdb_vendor => VMware
blockdevice_sdc_model => Virtual disk
blockdevice_sdc_size => 32212254720
blockdevice_sdc_vendor => VMware
blockdevice_sr0_model => VMware IDE CDR10
blockdevice_sr0_size => 64784384
blockdevice_sr0_vendor => NECVMWar
blockdevices => fd0,sda,sdb,sdc,sr0
boardmanufacturer => Intel Corporation
boardproductname => 440BX Desktop Reference Platform
boardserialnumber => None
domain => walgreens.com
facterversion => 1.7.6
filesystems => btrfs,ext2,ext3,ext4,msdos,vfat,xfs
fqdn => plin-w1rhns01.walgreens.com
hardwareisa => x86_64
hardwaremodel => x86_64
hostname => plin-w1rhns01
id => root
interfaces => ens192,lo
ipaddress => 172.23.27.50
ipaddress_ens192 => 172.23.27.50
ipaddress_lo => 127.0.0.1
is_virtual => true
kernel => Linux
kernelmajversion => 3.10
kernelrelease => 3.10.0-229.7.2.el7.x86_64
kernelversion => 3.10.0
macaddress => 00:50:56:b0:38:95
macaddress_ens192 => 00:50:56:b0:38:95
manufacturer => VMware, Inc.
memoryfree => 5.30 GB
memoryfree_mb => 5423.56
memorysize => 11.58 GB
memorysize_mb => 11855.77
memorytotal => 11.58 GB
netmask => 255.255.255.240
netmask_ens192 => 255.255.255.240
netmask_lo => 255.0.0.0
network_ens192 => 172.23.27.48
network_lo => 127.0.0.0
operatingsystem => RedHat
operatingsystemmajrelease => 7
operatingsystemrelease => 7.1
osfamily => RedHat
path => /usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
physicalprocessorcount => 1
processor0 => Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz
processor1 => Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz
processor2 => Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz
processor3 => Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz
processorcount => 4
productname => VMware Virtual Platform
ps => ps -ef
puppetversion => 3.6.2
rubysitedir => /usr/local/share/ruby/site_ruby/
rubyversion => 2.0.0
selinux => false
serialnumber => VMware-42 30 64 8e 9c 94 23 5f-10 74 90 7c 43 38 71 72
sshecdsakey => AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBDhZzl5vphjjEwK/YTEQz3KJ/x7XLGVHdzxg822WCBUAtIpReBtKiAhh7kG3RxfPZVADyp7HH7lB/xpieszs4jM=
sshfp_ecdsa => SSHFP 3 1 53dab70aa624092dc2722d1820025a19ddf35e69
SSHFP 3 2 fd3f2ed033a807937a3c5108f826ab8d5bafbf429586ba3a7459fa8d2f1b43c2
sshfp_rsa => SSHFP 1 1 e995b095b006a104a14021978285edf6c57463c3
SSHFP 1 2 cef9145ca9384e6f64e7fff844890e063f74e73d6956d1e5e9ba6605e1f534f0
sshrsakey => AAAAB3NzaC1yc2EAAAADAQABAAABAQDVL4fUsuSunC73keQbFq/RJUTejNrPELqiWchJhO8LaLR4FKHObQZh0pZHUybuItbhNu67rlrX7HTE6Pw2WuHObUCZysVBHkBg8Wni0oNMYlYadIDb//V4lCeBbuklGateQqsv+CgFvc3j3pcFgTvGy7WiSlVRjgyDHhQMiNf0CiBfiyuqoe2Pz+tY1ZbpZBa4KnJYW7EeFWdF8KX20hglE/geP/wqdCUL8+wdhHfYDG0l0uigtP9/yhOYf8g4klOZAQCp3741F+rjNsigTzxqiGZchbhRf1zIQ8c9He4G1jDV8AMGCm++UylzFhw4abvGaVLctnu/Cgsz4eKxY0DH
swapfree => 0.00 MB
swapfree_mb => 0.00
swapsize => 0.00 MB
swapsize_mb => 0.00
timezone => CDT
type => Other
uniqueid => 17ac321b
system_uptime => {"seconds"=>3663199, "hours"=>1017, "days"=>42, "uptime"=>"42 days"}
uptime => 42 days
uptime_days => 42
uptime_hours => 1017
uptime_seconds => 3663199
uuid => 4230648E-9C94-235F-1074-907C43387172
virtual => vmware
""".strip()


def test_facter():
    fc = Facter(context_wrap(FACTS))
    assert fc.uptime_days == "42"
    assert fc.fqdn == 'plin-w1rhns01.walgreens.com'
    assert fc.uuid == '4230648E-9C94-235F-1074-907C43387172'
    assert hasattr(fc, 'no_test') is False
    assert hasattr(fc, 'swapfree') is True
    assert fc.get('uptime') == "42 days"
    assert fc.get('dummy') is None
