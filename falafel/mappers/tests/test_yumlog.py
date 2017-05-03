from falafel.mappers.yumlog import YumLog
from falafel.mappers import ParseException
from falafel.tests import context_wrap

import unittest

OKAY = """
May 23 18:06:24 Installed: wget-1.14-10.el7_0.1.x86_64
Jan 24 00:24:00 Updated: glibc-2.12-1.149.el6_6.4.x86_64
Jan 24 00:24:09 Updated: glibc-devel-2.12-1.149.el6_6.4.x86_64
Jan 24 00:24:10 Updated: nss-softokn-3.14.3-19.el6_6.x86_64
Jan 24 18:10:05 Updated: 1:openssl-libs-1.0.1e-51.el7_2.5.x86_64
Jan 24 00:24:11 Updated: glibc-2.12-1.149.el6_6.4.i686
May 23 16:09:09 Erased: redhat-access-insights-batch
May 23 16:09:09 Erased: katello-agent
Jan 24 00:24:11 Updated: glibc-devel-2.12-1.149.el6_6.4.i686
""".strip()

ERROR = """
May 23 18:06:24 Installed: wget-1.14-10.el7_0.1.x86_64
Jan 24 00:24:00 Updated: glibc-2.12-1.149.el6_6.4.x86_64
Jan 24 00:24:09 Updated: glibc-devel-2.12-1.149.el6_6.4.x86_64
Bad
Jan 24 00:24:10 Updated: nss-softokn-3.14.3-19.el6_6.x86_64
Jan 24 18:10:05 Updated: 1:openssl-libs-1.0.1e-51.el7_2.5.x86_64
Jan 24 00:24:11 Updated: glibc-2.12-1.149.el6_6.4.i686
May 23 16:09:09 Erased: redhat-access-insights-batch
Jan 24 00:24:11 Updated: glibc-devel-2.12-1.149.el6_6.4.i686
""".strip()

THROWS_PARSEEXCEPTION = """
Jan 24 00:24:09 Updated:
"""


def test_iteration():
    yl = YumLog(context_wrap(OKAY))
    indices = [i.idx for i in yl]
    assert indices == range(len(yl))


def test_len():
    yl = YumLog(context_wrap(OKAY))
    assert len(yl) == 9


def test_present():
    yl = YumLog(context_wrap(OKAY))

    e = yl.present_packages.get('wget')
    assert e.pkg.name == 'wget'
    assert e.pkg.version == '1.14'

    e = yl.present_packages.get('openssl-libs')
    assert e.pkg.name == 'openssl-libs'
    assert e.pkg.version == '1.0.1e'


def test_error():
    yl = YumLog(context_wrap(ERROR))

    e = yl.present_packages.get('wget')
    assert e.pkg.name == 'wget'
    assert e.pkg.version == '1.14'

    e = yl.present_packages.get('openssl-libs')
    assert e.pkg.name == 'openssl-libs'
    assert e.pkg.version == '1.0.1e'

    assert len(yl) == 8


class test_throws_parseexception(unittest.TestCase):
    def test_exception_throwing(self):
        with self.assertRaisesRegexp(ParseException, 'YumLog could not parse'):
            yl = YumLog(context_wrap(THROWS_PARSEEXCEPTION))
            self.assertIsNone(yl)


def test_erased():
    yl = YumLog(context_wrap(OKAY))
    assert any(e.pkg.name == "redhat-access-insights-batch" for e in yl) is True
    assert any(e.pkg.name == "katello-agent" for e in yl) is True
