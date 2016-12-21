from falafel.mappers import lsof
from falafel.tests import context_wrap

LSOF = """
lsof: avoiding stat(/): -b was specified.
COMMAND     PID  TID           USER   FD      TYPE             DEVICE  SIZE/OFF       NODE NAME
systemd       1                root  cwd       DIR              253,1      4096        128 /
systemd       1                root  rtd       DIR              253,1      4096        128 /
systemd       1                root  txt       REG              253,1   1230920    1440410 /usr/lib/systemd/systemd
systemd       1                root  mem       REG              253,1     37152  135529970 /usr/lib64/libnss_sss.so.2
meventd     674  688           root  txt       REG              253,1     36344  135317954 /usr/sbin/dmeventd
dmeventd    674  688           root  mem       REG              253,1     20032  134413763 /usr/lib64/libuuid.so.1.3.0
dmeventd    674  688           root  mem       REG              253,1    248584  135108725 /usr/lib64/libblkid.so.1.1.0
bioset      611                root  txt   unknown                                         /proc/611/exe
""".strip()

LSOF_GOOD_V1 = """
COMMAND    PID  TID           USER   FD      TYPE             DEVICE  SIZE/OFF       NODE NAME
systemd-l  602                root   14u      CHR              13,64       0t0       6406 /dev/input/event0
systemd-l  602                root   15u      CHR              13,65       0t0       6407 /dev/input/event1
systemd-l  602                root   16u      CHR                4,6       0t0       4694 /dev/tty6
dbus-daem  603                dbus    0r      CHR                1,3       0t0       4674 /dev/null
dbus-daem  603  615           dbus    0r      CHR                1,3       0t0       4674 /dev/null
abrt-watc 8619                root    0r      CHR                1,3       0t0       4674 /dev/null
wpa_suppl  641                root    0r      CHR                1,3       0t0       4674 /dev/null
polkitd    642             polkitd    0u      CHR                1,3       0t0       4674 /dev/null
polkitd    642             polkitd    1u      CHR                1,3       0t0       4674 /dev/null
polkitd    642             polkitd    2u      CHR                1,3       0t0       4674 /dev/null
gmain      642  643        polkitd    0u      CHR                1,3       0t0       4674 /dev/null
gmain      642  643        polkitd    1u      CHR                1,3       0t0       4674 /dev/null
gmain      642  643        polkitd    2u      CHR                1,3       0t0       4674 /dev/null
gdbus      642  646        polkitd    0u      CHR                1,3       0t0       4674 /dev/null
gdbus      642  646        polkitd    1u      CHR                1,3       0t0       4674 /dev/null
gdbus      642  646        polkitd    2u      CHR                1,3       0t0       4674 /dev/null
JS         642  648        polkitd    1r      BLK               8,16       0t0      16884 /dev/sda
JS         642  648        polkitd    1u      CHR                1,3       0t0       4674 /dev/null
JS         642  648        polkitd    2u      CHR                1,3       0t0       4674 /dev/null
""".strip()

columns = ["COMMAND", "PID", "TID", "USER", "FD", "TYPE", "DEVICE", "SIZE/OFF", "NODE", "NAME"]


def test_lsof():
    mapper = lsof.Lsof(context_wrap(LSOF))
    d = list(mapper)

    assert set(columns) == set([k for f in d for k in f.keys()])
    assert d[0] == {
        "COMMAND": "systemd",
        "PID": "1",
        "TID": "",
        "USER": "root",
        "FD": "cwd",
        "TYPE": "DIR",
        "DEVICE": "253,1",
        "SIZE/OFF": "4096",
        "NODE": "128",
        "NAME": "/"
    }

    # Spot checks
    assert d[3]["TID"] == ""
    assert d[4]["TID"] == "688"
    assert d[5]["TYPE"] == "REG"
    assert d[7]["NAME"] == "/proc/611/exe"

    assert d[-1] == {
        "COMMAND": "bioset",
        "PID": "611",
        "TID": "",
        "USER": "root",
        "FD": "txt",
        "TYPE": "unknown",
        "DEVICE": "",
        "SIZE/OFF": "",
        "NODE": "",
        "NAME": "/proc/611/exe"
    }


def test_lsof_good():
    mapper = lsof.Lsof(context_wrap(LSOF_GOOD_V1))
    d = list(mapper)
    assert d[0] == {
        "COMMAND": "systemd-l",
        "PID": "602",
        "TID": "",
        "USER": "root",
        "FD": "14u",
        "TYPE": "CHR",
        "DEVICE": "13,64",
        "SIZE/OFF": "0t0",
        "NODE": "6406",
        "NAME": "/dev/input/event0"
    }

    # Spot checks
    assert d[3]["TID"] == ""
    assert d[4]["TID"] == "615"
    assert d[5]["COMMAND"] == "abrt-watc"
    assert d[5]["PID"] == "8619"
    assert d[5]["TYPE"] == "CHR"
    assert d[7]["NAME"] == "/dev/null"

    assert d[-1] == {
        "COMMAND": "JS",
        "PID": "642",
        "TID": "648",
        "USER": "polkitd",
        "FD": "2u",
        "TYPE": "CHR",
        "DEVICE": "1,3",
        "SIZE/OFF": "0t0",
        "NODE": "4674",
        "NAME": "/dev/null"
    }
