import pytest

from insights.tests import context_wrap
from insights.parsers.alternatives import AlternativesOutput, JavaAlternatives
from insights.core import ParseException

ALT_MTA = """
mta - status is auto.
 link currently points to /usr/sbin/sendmail.postfix
/usr/sbin/sendmail.postfix - priority 30
 slave mta-mailq: /usr/bin/mailq.postfix
 slave mta-newaliases: /usr/bin/newaliases.postfix
Current `best' version is /usr/sbin/sendmail.postfix.
"""

DUPLICATED_STATUS_LINE = """
mta - status is auto.
Nonsense line that should be ignored
mta - status is auto.
"""

MISSING_STATUS_LINE = """
 link currently points to /usr/sbin/sendmail.postfix
/usr/sbin/sendmail.postfix - priority 30
 slave mta-mailq: /usr/bin/mailq.postfix
 slave mta-newaliases: /usr/bin/newaliases.postfix
Current `best' version is /usr/sbin/sendmail.postfix.
"""


def test_mta_alternatives():
    mtas = AlternativesOutput(context_wrap(ALT_MTA))

    assert hasattr(mtas, 'program')
    assert mtas.program == 'mta'
    assert hasattr(mtas, 'status')
    assert mtas.status == 'auto'
    assert hasattr(mtas, 'link')
    assert mtas.link == '/usr/sbin/sendmail.postfix'
    assert hasattr(mtas, 'best')
    assert mtas.best == '/usr/sbin/sendmail.postfix'

    assert hasattr(mtas, 'paths')
    assert isinstance(mtas.paths, list)
    assert len(mtas.paths) == 1

    for i in ('path', 'priority', 'slave'):
        assert i in mtas.paths[0]


def test_failure_modes():
    # Duplicate status line raises ParseException
    with pytest.raises(ParseException, match='Program line for mta'):
        alts = AlternativesOutput(context_wrap(DUPLICATED_STATUS_LINE))
        assert alts.program is None

    # Missing status line results in no data
    alts = AlternativesOutput(context_wrap(MISSING_STATUS_LINE))
    for i in (alts.program, alts.status, alts.link, alts.best):
        assert i is None
    assert alts.paths == []


alter_java = """
java - status is auto.
 link currently points to /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java
/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java - priority 16091
 slave ControlPanel: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/ControlPanel
 slave keytool: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/keytool
 slave policytool: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/policytool
 slave rmid: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/rmid
 slave rmiregistry: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/rmiregistry
 slave tnameserv: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/tnameserv
 slave jre_exports: /usr/lib/jvm-exports/jre-1.6.0-ibm.x86_64
 slave jre: /usr/lib/jvm/jre-1.6.0-ibm.x86_64
/usr/lib/jvm/jre-1.4.2-gcj/bin/java - priority 1420
 slave ControlPanel: (null)
 slave keytool: /usr/lib/jvm/jre-1.4.2-gcj/bin/keytool
 slave policytool: (null)
 slave rmid: (null)
 slave rmiregistry: /usr/lib/jvm/jre-1.4.2-gcj/bin/rmiregistry
 slave tnameserv: (null)
 slave jre_exports: /usr/lib/jvm-exports/jre-1.4.2-gcj
 slave jre: /usr/lib/jvm/jre-1.4.2-gcj
Current `best' version is /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java.
""".strip().encode('utf8')

alter_no_java = """
/usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/java - priority 170079
 slave ControlPanel: (null)
 slave keytool: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/keytool
 slave orbd: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/orbd
 slave pack200: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/pack200
 slave policytool: (null)
 slave rmid: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/rmid
 slave rmiregistry: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/rmiregistry
 slave servertool: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/servertool
 slave tnameserv: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/tnameserv
 slave unpack200: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/unpack200
 slave jre_exports: /usr/lib/jvm-exports/jre-1.7.0-openjdk.x86_64
 slave jre: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64
 slave java.1.gz: /usr/share/man/man1/java-java-1.7.0-openjdk.1.gz
 slave keytool.1.gz: /usr/share/man/man1/keytool-java-1.7.0-openjdk.1.gz
 slave orbd.1.gz: /usr/share/man/man1/orbd-java-1.7.0-openjdk.1.gz
 slave pack200.1.gz: /usr/share/man/man1/pack200-java-1.7.0-openjdk.1.gz
 slave rmid.1.gz: /usr/share/man/man1/rmid-java-1.7.0-openjdk.1.gz
 slave rmiregistry.1.gz: /usr/share/man/man1/rmiregistry-java-1.7.0-openjdk.1.gz
 slave servertool.1.gz: /usr/share/man/man1/servertool-java-1.7.0-openjdk.1.gz
 slave tnameserv.1.gz: /usr/share/man/man1/tnameserv-java-1.7.0-openjdk.1.gz
 slave unpack200.1.gz: /usr/share/man/man1/unpack200-java-1.7.0-openjdk.1.gz
Current `best' version is /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/java.
""".strip().encode('utf8')


def test_class_no_java():
    java = JavaAlternatives(context_wrap(alter_no_java))
    for i in (java.program, java.status, java.link, java.best):
        assert i is None
    assert java.paths == []


def test_class_has_java():
    java = JavaAlternatives(context_wrap(alter_java))

    assert java.program == 'java'
    assert java.status == 'auto'
    assert java.link == '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java'
    assert java.best == '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java'

    assert isinstance(java.paths, list)
    assert len(java.paths) == 2

    for i in ('path', 'priority', 'slave'):
        assert i in java.paths[0]

    assert java.paths[0]['path'] == '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java'
    assert java.paths[0]['priority'] == 16091
    assert isinstance(java.paths[0]['slave'], dict)
    assert sorted(java.paths[0]['slave'].keys()) == sorted([
        'ControlPanel', 'keytool', 'policytool', 'rmid', 'rmiregistry',
        'tnameserv', 'jre_exports', 'jre'
    ])
    assert java.paths[0]['slave']['ControlPanel'] == '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/ControlPanel'

    for i in ('path', 'priority', 'slave'):
        assert i in java.paths[1]

    assert java.paths[1]['path'] == '/usr/lib/jvm/jre-1.4.2-gcj/bin/java'
    assert java.paths[1]['priority'] == 1420
    assert isinstance(java.paths[1]['slave'], dict)
    assert sorted(java.paths[1]['slave'].keys()) == sorted([
        'ControlPanel', 'keytool', 'policytool', 'rmid', 'rmiregistry',
        'tnameserv', 'jre_exports', 'jre'
    ])
    assert java.paths[1]['slave']['ControlPanel'] == '(null)'
