from .. import LogFileOutput, mapper


@mapper('foreman_satellite.log')
class SatelliteLog(LogFileOutput):
    pass


@mapper('foreman_production.log')
class ProductionLog(LogFileOutput):
    pass


@mapper('candlepin.log')
class CandlepinLog(LogFileOutput):
    pass
