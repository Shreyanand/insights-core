from .. import LogFileOutput, mapper


@mapper('cinder_volume.log')
class CinderVolumeLog(LogFileOutput):
    pass
