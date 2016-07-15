from falafel.mappers import hostname
from falafel.tests import context_wrap

HOSTNAME = "rhel7.example.com"


class TestHostname():
    def test_hostname(self):
        data = hostname.common(context_wrap(HOSTNAME))
        assert len(data) == 4
        assert data.get('fqdn') == "rhel7.example.com"
        assert data.get('hostname') == "rhel7"
