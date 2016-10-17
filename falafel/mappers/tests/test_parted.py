"""
``test parted``
===============
"""
import pytest

from falafel.core.context import Context
from falafel.mappers import ParseException
from falafel.mappers.parted import PartedL

PARTED_DATA = """
Model: Virtio Block Device (virtblk)
Disk /dev/vda: 9664MB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags:

Number  Start   End     Size    Type     File system  Flags
 1      1049kB  525MB   524MB   primary  xfs          boot
 2      525MB   9664MB  9138MB  primary               lvm
""".strip()

PARTED_DATA_2 = """
Model: IBM 2107900 (scsi)
Disk /dev/sdet: 2147MB
Sector size (logical/physical): 512B/512B
Partition Table: msdos

Number  Start   End     Size    Type     File system  Flags
 1      32.3kB  2580kB  2548kB  primary
""".strip()

PARTED_DATA_3 = """
Model: DELL PERC H710 (scsi)
Disk /dev/sda: 292GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos

Number  Start   End     Size    Type      File system  Flags
 1      32.3kB  526MB   526MB   primary   ext3         boot
 2      526MB   9114MB  8587MB  primary   linux-swap
 3      9114MB  12.3GB  3224MB  primary   ext3
 4      12.3GB  292GB   280GB   extended
 5      12.3GB  254GB   241GB   logical   ext3
 6      254GB   281GB   26.8GB  logical   ext3
 7      281GB   285GB   4294MB  logical   ext3
 8      285GB   288GB   3224MB  logical   ext3
 9      288GB   290GB   2147MB  logical   ext3
10      290GB   292GB   2147MB  logical   ext3
""".strip()

PARTED_ERR_DATA = ['Error: /dev/dm-1: unrecognised disk label']

PARTED_ERR_DATA_2 = """
Model: IBM 2107900 (scsi)
Sector size (logical/physical): 512B/512B
Partition Table: msdos

Number  Start   End     Size    Type     File system  Flags
 1      32.3kB  2580kB  2548kB  primary
""".strip()


def test_parted():
    context = Context(content=PARTED_DATA.splitlines())
    results = PartedL(context)
    assert results is not None
    assert results.get('model') == 'Virtio Block Device (virtblk)'
    assert results.disk == '/dev/vda'
    assert results.get('size') == '9664MB'
    assert results.get('sector_size') == '512B/512B'
    assert results.logical_sector_size == '512B'
    assert results.physical_sector_size == '512B'
    assert results.get('partition_table') == 'msdos'
    assert results.get('disk_flags') is None
    partitions = results.partitions
    assert len(partitions) == 2
    assert partitions[0].number == '1'
    assert partitions[0].start == '1049kB'
    assert partitions[0].end == '525MB'
    assert partitions[0].size == '524MB'
    assert partitions[0].file_system == 'xfs'
    assert partitions[0].get('name') is None
    assert partitions[0].type == 'primary'
    assert partitions[0].flags == 'boot'
    assert results.boot_partition is not None
    assert results.boot_partition.number == '1'

    assert partitions[1].get('file_system') == 'lvm'
    assert partitions[1].get('flags') == 'lvm'
    assert partitions[1].get('name') is None
    assert partitions[1].get('number') == '2'
    assert partitions[1].get('start') == '525MB'
    assert partitions[1].get('end') == '9664MB'
    assert partitions[1].get('size') == '9138MB'
    assert partitions[1].get('type') == 'primary'

    context = Context(content=PARTED_DATA_2.splitlines())
    results = PartedL(context)
    assert results is not None
    assert results.disk == '/dev/sdet'
    assert len(results.partitions) == 1

    context = Context(content=PARTED_DATA_3.splitlines())
    results = PartedL(context)
    assert results is not None
    assert results.disk == '/dev/sda'
    assert results.logical_sector_size == '512B'
    assert results.physical_sector_size == '512B'
    assert len(results.partitions) == 10

    context = Context(content=PARTED_ERR_DATA)
    with pytest.raises(ParseException):
        PartedL(context)

    context = Context(content=PARTED_ERR_DATA_2.splitlines())
    with pytest.raises(ParseException):
        PartedL(context)
