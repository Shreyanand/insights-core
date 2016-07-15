from falafel.mappers.hosts import hosts
from falafel.tests import context_wrap

HOSTS_EXAMPLE = """
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4
::1 localhost localhost.localdomain localhost6 localhost6.localdomain6

# Comment
127.0.0.1 fte.foo.redhat.com ci.foo.redhat.com qa.foo.redhat.com stage.foo.redhat.com prod.foo.redhat.com # Comment at end of line
""".strip()

EXPECTED = {
    "127.0.0.1": [
        "localhost",
        "localhost.localdomain",
        "localhost4",
        "localhost4.localdomain4",
        "fte.foo.redhat.com",
        "ci.foo.redhat.com",
        "qa.foo.redhat.com",
        "stage.foo.redhat.com",
        "prod.foo.redhat.com"
    ],
    "::1": [
        "localhost",
        "localhost.localdomain",
        "localhost6",
        "localhost6.localdomain6"
    ]
}


def test_hosts():
    d = hosts(context_wrap(HOSTS_EXAMPLE)).data
    assert len(d) == 2
    for key in ["127.0.0.1", "::1"]:
        assert key in d
        assert d[key] == EXPECTED[key]


def test_all_hosts():
    all_names = hosts(context_wrap(HOSTS_EXAMPLE)).all_names
    expected = set(EXPECTED["127.0.0.1"]) | set(EXPECTED["::1"])
    assert all_names == expected
