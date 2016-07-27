import os
from falafel.core.plugins import mapper
from falafel.core import MapperOutput, computed


class HTTPDConf(MapperOutput):

    def __init__(self, context):
        self.data = context.content
        self.path = context.path
        self.computed = {}
        self.compute()

    @computed
    def file_path(self):
        """
        Returns the file path of this httpd.conf
        """
        return self.path

    @computed
    def file_name(self):
        """
        Returns the file name of this httpd.conf
        """
        return os.path.basename(self.path)

    def get_filter_strings(self, filter_string):
        """
        Get the filter_string directive options (should not be empty) string
        (remove extra spaces and convert to lowercase) and wrap them into a list
        """
        result = []
        for line in self.data:
            if not line or line.lstrip().startswith('#'):
                continue
            if filter_string in line:
                options = " ".join(line.split(filter_string, 1)[1].split()).lower()
                if options:
                    result.append(options)
        self._add_to_computed(filter_string, result)
        return result


# adding filters for mappers, need to adjust it when using
# maybe could remove it when unmaintainable
@mapper('httpd.conf', ["SSL", "NSSProtocol", "MaxClients"])
@mapper('httpd.conf.d', ["SSL", "NSSProtocol", "MaxClients"])
def parse_httpd_conf(context):
    """
    Get these three basic filter string according to exsited rules.
    Can add more filter conditions if needed.

    return a HTTPDConf object
    """
    return HTTPDConf(context)
