from falafel.mappers import hostname
from falafel.tests import context_wrap

HOSTNAME = "rhel7.example.com"


class TestHostname():
    def test_hostname(self):
        data = hostname.hostname(context_wrap(HOSTNAME))
        assert data.fqdn == "rhel7.example.com"
        assert data.hostname == "rhel7"
        assert data.domain == "example.com"
