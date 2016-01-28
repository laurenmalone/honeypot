import os
import sys

path = "plugins/"
plugins = {}

sys.path.insert(0, path)
for i in os.listdir(path):
    fname, ext = os.path.splitext(i)
    if ext == '.py':
        mod = __import__(fname)
        plugins[fname] = mod.Plugin()
sys.path.pop(0)

for plugin in plugins.values():
    plugin.run()

