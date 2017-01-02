from falafel.mappers.hostname import Hostname
from falafel.tests import context_wrap

HOSTNAME = "rhel7.example.com"
HOSTNAME_SHORT = "rhel7"


def test_hostname():
    data = Hostname(context_wrap(HOSTNAME))
    assert data.fqdn == "rhel7.example.com"
    assert data.hostname == "rhel7"
    assert data.domain == "example.com"

    data = Hostname(context_wrap(HOSTNAME_SHORT))
    assert data.fqdn == "rhel7"
    assert data.hostname == "rhel7"
    assert data.domain == ""

    data = Hostname(context_wrap(""))
    assert data.fqdn is None
    assert data.hostname is None
    assert data.domain is None
