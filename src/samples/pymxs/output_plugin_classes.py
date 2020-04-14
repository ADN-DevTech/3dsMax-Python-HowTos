'''
    Demonstrates using the PluginManager to extract information about loaded
    plugins.
'''
from pymxs import runtime as rt # pylint: disable=import-error

# List all plug-in dlls
PLUGIN_COUNT = rt.pluginManager.pluginDllCount
print(f"Total PluginDlls: {PLUGIN_COUNT}\n")
# maxscript uses one based indices
for p in range(1, PLUGIN_COUNT + 1):
    print("PluginDll:", rt.pluginManager.pluginDllFullPath(p))
    print("Description:", rt.pluginManager.pluginDllName(p))
    print("Loaded:", rt.pluginManager.isPluginDllLoaded(p))
