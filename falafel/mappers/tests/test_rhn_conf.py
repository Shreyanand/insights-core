from falafel.mappers import rhn_conf
from falafel.tests import context_wrap

RHN_TEST = """
a=1
b = 2

#c = 3
c = include an = sign
server.satellite.http_proxy = corporate_gateway.example.com:8080
server.satellite.http_proxy_username =
server.satellite.http_proxy_password =

traceback_mail = test@pobox.com, test@redhat.com

web.default_taskmaster_tasks = RHN::Task::SessionCleanup, RHN::Task::ErrataQueue,
    RHN::Task::ErrataEngine,
    RHN::Task::DailySummary, RHN::Task::SummaryPopulation,
    RHN::Task::RHNProc,
    RHN::Task::PackageCleanup
""".strip()


class TestRhnConf():
    def test_rhn_conf(self):
        r = rhn_conf.rhn_conf(context_wrap(RHN_TEST))
        assert len(r) == 8
        assert r["a"] == "1"
        assert r["b"] == "2"
        assert r["c"] == "include an = sign"
        assert r["server.satellite.http_proxy_username"] == ""
        assert r["traceback_mail"] == ['test@pobox.com', 'test@redhat.com']
        assert r["web.default_taskmaster_tasks"] == \
            ['RHN::Task::SessionCleanup', 'RHN::Task::ErrataQueue',
             'RHN::Task::ErrataEngine', 'RHN::Task::DailySummary',
             'RHN::Task::SummaryPopulation', 'RHN::Task::RHNProc',
             'RHN::Task::PackageCleanup']
