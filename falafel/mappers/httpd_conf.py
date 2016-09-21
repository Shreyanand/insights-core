from .. import MapperOutput, mapper, get_active_lines


@mapper('httpd.conf')
@mapper('httpd.conf.d')
class HttpdConf(MapperOutput):

    @staticmethod
    def parse_content(content):
        """
            Get the filter_string directive options (should not be empty) string
            (remove extra spaces and convert to lowercase) and wrap them into a list
            Add the parsing of "<IfModule prefork.c>" and "<IfModule worker.c>"
            sections
        """
        result = {}
        sect = None
        for line in get_active_lines(content):
            try:
                # new IfModule section start
                if line.startswith('<IfModule'):
                    if 'prefork.c' in line:
                        sect = 'MPM_prefork'
                    elif 'worker.c' in line:
                        sect = 'MPM_worker'
                # section end
                elif line.startswith('</IfModule'):
                    sect = None
                else:
                    k, rest = line.split(None, 1)
                    if sect:
                        if sect not in result:
                            result[sect] = {k: rest}
                        else:
                            result[sect][k] = rest
                    else:
                        result[k] = rest
            except Exception:
                pass
        return result
