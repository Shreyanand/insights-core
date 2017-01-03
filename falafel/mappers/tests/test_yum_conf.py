from falafel.mappers.yum_conf import YumConf
from falafel.tests import context_wrap


YUM_CONF = """
[main]
cachedir=/var/cache/yum/$basearch/$releasever
keepcache=0
debuglevel=2
logfile=/var/log/yum.log
exactarch=1
obsoletes=1
gpgcheck=1
plugins=1
installonly_limit=3

#  This is the default, if you make this bigger yum won't see if the metadata
# is newer on the remote and so you'll "gain" the bandwidth of not having to
# download the new metadata and "pay" for it by yum not having correct
# information.
#  It is esp. important, to have correct metadata, for distributions like
# Fedora which don't keep old packages around. If you don't like this checking
# interupting your command line usage, it's much better to have something
# manually check the metadata once an hour (yum-updatesd will do this).
# metadata_expire=90m

# PUT YOUR REPOS HERE OR IN separate files named file.repo
# in /etc/yum.repos.d
"""


CONF_PATH = 'etc/yum.conf'


def test_get_yum_conf():
    yum_conf = YumConf(context_wrap(YUM_CONF, path=CONF_PATH))

    print yum_conf.get('main')
    assert yum_conf.get('main') == {
        'plugins': '1',
        'keepcache': '0',
        'cachedir': '/var/cache/yum/$basearch/$releasever',
        'exactarch': '1',
        'obsoletes': '1',
        'installonly_limit': '3',
        'debuglevel': '2',
        'gpgcheck': '1',
        'logfile': '/var/log/yum.log'
    }
    assert yum_conf.file_name == 'yum.conf'
    assert yum_conf.file_path == 'etc/yum.conf'
