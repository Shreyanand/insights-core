from falafel.core.plugins import mapper
from falafel.core import MapperOutput
from falafel.mappers import get_active_lines


class HTTPDConf(MapperOutput):
    pass

# Expandable list of custom delimiters
# Default is space
DELIMS = {
    "SSLCipherSuite": ":",
    "NSSProtocol": ","
}


def parse(content):
    """
    Get the filter_string directive options (should not be empty) string
    (remove extra spaces and convert to lowercase) and wrap them into a list
    """
    result = {}
    sect = None
    for line in get_active_lines(content):
        try:
            # new section start
            if line.startswith('<'):
                sect = line.strip('<>')
            # section end
            elif line.startswith('</'):
                sect = None
            else:
                k, rest = line.split(None, 1)
                if sect:
                    if sect not in result:
                        result[sect] = {k: rest}
                    else:
                        result[sect][k] = rest
                else:
                    result[k] = [s.strip().lower() for s in rest.split(DELIMS.get(k))]
        except Exception:
            pass
    return result


@mapper('httpd.conf')
@mapper('httpd.conf.d')
def parse_httpd_conf(context):
    """
    Get these three basic filter string according to exsited rules.
    Can add more filter conditions if needed.

    return a HTTPDConf object
    """
    d = parse(context.content)
    if d:  # i.e. if we got any lines parsed successfully
        return HTTPDConf(d, path=context.path)
