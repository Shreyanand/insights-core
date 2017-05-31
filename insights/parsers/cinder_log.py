from .. import LogFileOutput, parser


@parser('cinder_volume.log')
class CinderVolumeLog(LogFileOutput):
    pass
