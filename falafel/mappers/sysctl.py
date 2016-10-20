from .. import Mapper, LogFileOutput, mapper
from ..mappers import split_kv_pairs


@mapper('sysctl.conf')
class SysctlConf(Mapper):
    """Parse `/etc/sysctl.conf` file

    Sample input::

        # sysctl.conf sample
        #
          kernel.domainname = example.com

        ; this one has a space which will be written to the sysctl!
          kernel.modprobe = /sbin/mod probe

    Attributes
    ----------
    data: OrderedDict
        Dictionary containing key/value pairs for the lines in the
        configuration file.  Dictionary is in order keywords first
        appear in the lines.

    Examples
    --------
    >>> shared[SysctlConf].data['kernel.domainname']
    'example.com'
    >>> shared[SysctlConf].data['kernel.modprobe']
    '/sbin/mod probe'
    """

    def parse_content(self, content):
        # Valid comments are both # and ; so remove one locally,
        # other comments and blank lines are removed by split fxn.
        lines = [l for l in content if not l.strip().startswith(';')]
        self.data = split_kv_pairs(lines, ordered=True)


@mapper('sysctl')
class Sysctl(Mapper):

    def parse_content(self, content):
        """
        r = {}
        for line in content:
            if "=" not in line:
                continue

            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            r[k] = v
        self.data = r
        """
        self.data = split_kv_pairs(content)


@mapper("sysctl.conf_initramfs")
class SysctlConfInitramfs(LogFileOutput):
    """Shared mapper for the output of ``lsinitrd`` applied to kdump
    initramfs images to view ``sysctl.conf`` and ``sysctl.d``
    configurations.

    For now, the file is treated as raw lines (as a ``LogFileOutput``
    mapper.  This is because the output of the command, applied to
    multiple files to examine multiple files does not seem to be
    unambiguously parsible.

    Since the only plugins requireing the file to date "grep out"
    certain strings, this approach will suffice.
    """
    pass


@mapper('sysctl')
def runtime(context):
    """Deprecated, do not use."""
    return Sysctl(context).data
