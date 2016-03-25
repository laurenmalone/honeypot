from plugin_template import Template


class Plugin(Template):

    def __init__(self):
        Template.__init__(self)
        self.geo_ip = None
        self.PORT = None
        self.geoIp_feature_json_string = None
        self.description = None
        self.ORM = None
        self.value = None
        self.display = None

    def run(self):
        return self.PORT

    def test(self):
        print self.PORT

Plugin.test(Plugin())
