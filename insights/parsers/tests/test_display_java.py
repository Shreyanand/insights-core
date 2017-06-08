from insights.tests import context_wrap
from insights.parsers.display_java import default_java, JavaAlternatives

import unittest

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


def test_no_java():
    java = default_java(context_wrap(alter_no_java))
    assert java is None


def test_has_java():
    java = default_java(context_wrap(alter_java))
    assert java == "/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java"


class Test_Class(unittest.TestCase):

    def test_class_no_java(self):
        java = JavaAlternatives(context_wrap(alter_no_java))
        self.assertTrue(hasattr(java, 'program'))
        self.assertIsNone(java.program)
        # Direct access
        self.assertTrue(hasattr(java, 'status'))
        self.assertIsNone(java.status)
        self.assertTrue(hasattr(java, 'link'))
        self.assertIsNone(java.link)
        self.assertTrue(hasattr(java, 'paths'))
        self.assertEqual(java.paths, [])
        self.assertTrue(hasattr(java, 'best'))
        self.assertIsNone(java.best)

    def test_class_has_java(self):
        java = JavaAlternatives(context_wrap(alter_java))

        self.assertTrue(hasattr(java, 'program'))
        self.assertEqual(java.program, 'java')
        self.assertTrue(hasattr(java, 'status'))
        self.assertEqual(java.status, 'auto')
        self.assertTrue(hasattr(java, 'link'))
        self.assertEqual(java.link, '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java')
        self.assertTrue(hasattr(java, 'best'))
        self.assertEqual(java.best, '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java')

        self.assertTrue(hasattr(java, 'paths'))
        self.assertIsInstance(java.paths, list)
        self.assertEqual(len(java.paths), 2)

        self.assertIn('path', java.paths[0])
        self.assertIn('priority', java.paths[0])
        self.assertIn('slave', java.paths[0])
        self.assertEqual(java.paths[0]['path'], '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java')
        self.assertEqual(java.paths[0]['priority'], 16091)
        self.assertIsInstance(java.paths[0]['slave'], dict)
        self.assertEqual(sorted(java.paths[0]['slave'].keys()), sorted([
            'ControlPanel', 'keytool', 'policytool', 'rmid', 'rmiregistry',
            'tnameserv', 'jre_exports', 'jre'
        ]))
        self.assertEqual(java.paths[0]['slave']['ControlPanel'], '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/ControlPanel')

        self.assertIn('path', java.paths[1])
        self.assertIn('priority', java.paths[1])
        self.assertIn('slave', java.paths[1])
        self.assertEqual(java.paths[1]['path'], '/usr/lib/jvm/jre-1.4.2-gcj/bin/java')
        self.assertEqual(java.paths[1]['priority'], 1420)
        self.assertIsInstance(java.paths[1]['slave'], dict)
        self.assertEqual(sorted(java.paths[1]['slave'].keys()), sorted([
            'ControlPanel', 'keytool', 'policytool', 'rmid', 'rmiregistry',
            'tnameserv', 'jre_exports', 'jre'
        ]))
        self.assertEqual(java.paths[1]['slave']['ControlPanel'], '(null)')
