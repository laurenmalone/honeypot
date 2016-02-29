from threading import Thread


class PluginManager:
    def __init__(self, plugin, session_factory):
        self._plugin = plugin
        self._session_factory = session_factory

    def run(self):
        pass

    def stop(self):
        pass

