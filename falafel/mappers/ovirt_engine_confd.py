from falafel.core.plugins import mapper
from falafel.core import MapperOutput


@mapper("ovirt_engine_confd")
def ovirt_engine_confd(context):
    d = {k.strip('" '): v.strip('" ') for k, _, v in [l.partition("=") for l in context.content]}
    return MapperOutput(d)
