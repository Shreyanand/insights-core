from falafel.mappers import hostname
from falafel.tests import context_wrap

HOSTNAME = "rhel7.example.com"
HOSTNAME_SHORT = "rhel7"
FACTS_FQDN = """
COMMAND> facter

architecture => x86_64
augeasversion => 1.1.0
facterversion => 1.7.6
filesystems => xfs
fqdn => ewa-satellite.cs.boeing.com
domain => cs.boeing.com
""".strip()
FACTS_NO_FQDN = """
COMMAND> facter

architecture => x86_64
facterversion => 1.7.6
filesystems => xfs
""".strip()


class TestHostname():
    def test_hostname(self):
        data = hostname.Hostname(context_wrap(HOSTNAME))
        assert data.fqdn == "rhel7.example.com"
        assert data.hostname == "rhel7"
        assert data.domain == "example.com"

        data = hostname.Hostname(context_wrap(HOSTNAME_SHORT))
        assert data.fqdn == "rhel7"
        assert data.hostname == "rhel7"
        assert data.domain == ""

        data = hostname.Hostname(context_wrap(FACTS_FQDN))
        assert data.fqdn == "ewa-satellite.cs.boeing.com"
        assert data.hostname == "ewa-satellite"
        assert data.domain == "cs.boeing.com"

        data = hostname.Hostname(context_wrap(FACTS_NO_FQDN))
        assert data.fqdn is None
        assert data.hostname is None
        assert data.domain is None

        data = hostname.Hostname(context_wrap(""))
        assert data.fqdn is None
        assert data.hostname is None
        assert data.domain is None
