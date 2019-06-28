from . import lib
import pyblish.api
import pyblish.util
import pyblish.plugin
from pype.lib import filter_pyblish_plugins
import os


def test_pyblish_plugin_filter(printer, monkeypatch):
    """
    Test if pyblish filter can filter and modify plugins on-the-fly.
    """

    lib.setup_empty()
    monkeypatch.setitem(os.environ, 'PYBLISHPLUGINPATH', '')
    plugins = pyblish.api.registered_plugins()
    printer("Test if we have no registered plugins")
    assert len(plugins) == 0
    paths = pyblish.api.registered_paths()
    printer("Test if we have no registered plugin paths")
    print(paths)

    class MyTestPlugin(pyblish.api.InstancePlugin):
        my_test_property = 1
        label = "Collect Renderable Camera(s)"
        hosts = ["test"]
        families = ["default"]

    pyblish.api.register_host("test")
    pyblish.api.register_plugin(MyTestPlugin)
    pyblish.api.register_discovery_filter(filter_pyblish_plugins)
    plugins = pyblish.api.discover()

    printer("Test if only one plugin was discovered")
    assert len(plugins) == 1
    printer("Test if properties are modified correctly")
    assert plugins[0].label == "loaded from preset"
    assert plugins[0].families == ["changed", "by", "preset"]
    assert plugins[0].optional is True

    lib.teardown()
