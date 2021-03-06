# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

# YAMl
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from twisted.application.internet import TCPClient, TCPServer

from cloudbox.common.loops import LoopRegistry
from cloudbox.common.constants.common import *


class cloudBoxService(object):
    """
    The central hub of all services.
    """

    def __init__(self, whoami):
        """
        Initializes the service.
        Whoami contains the server identifier.
        """
        if whoami not in SERVER_TYPES:
            raise ValueError("Server not in valid SERVER_TYPE")
        self.serverType = SERVER_TYPES[whoami]
        # Make our loop registry
        self.loops = LoopRegistry()
        self.factories = {}
        self.settings = {}

    def getServerType(self):
        return self.serverType

    def loadConfig(self, reload=False):
        """
        Loads the configuration file, depending on the SERVER_TYPE of the server.
        Specify reload to make the function reload the configuration. Note that by specifying reload, the function
        assumes that the related factories exist.
        """
        if self.serverType == SERVER_TYPES["HubServer"]:
            with open("config/hub.yaml", "r") as f:
                s = f.read()
            self.settings["hub"] = yaml.load(s, Loader)
        elif self.serverType == SERVER_TYPES["DatabaseServer"]:
            with open("config/database.yaml", "r") as f:
                s = f.read()
            self.settings["db"] = yaml.dump(yaml.load(s, Loader))
        elif self.serverType == SERVER_TYPES["DatabaseServer"]:
            with open("config/world.yaml", "r") as f:
                s = f.read()
            self.settings["world"] = yaml.dump(yaml.load(s, Loader))
        self.populateConfig(reload)

    def populateConfig(self, reload=False):
        # Send the configuration to the respective factories
        if self.serverType == SERVER_TYPES["HubServer"]:
            self.factories["MinecraftHubServerFactory"].settings = self.settings["hub"]
            self.factories["WorldServerCommServerFactory"].settings = self.settings["hub"]

    def start(self):
        """
        Initializes components as needed.
        """
        if self.serverType == SERVER_TYPES["HubServer"]:
            from cloudbox.hub.run import init as hubInit
            hubInit(self)
        elif self.serverType == SERVER_TYPES["DatabaseServer"]:
            from cloudbox.database.server.run import init as dbInit
            dbInit(self)
        elif self.serverType == SERVER_TYPES["WorldServer"]:
            from cloudbox.world.run import init as worldInit
            worldInit(self)

    def stop(self):
        """
        Initializes components as needed.
        """
        if self.serverType == SERVER_TYPES["HubServer"]:
            from cloudbox.hub.run import shutdown as hubShutdown
            hubShutdown(self)
        elif self.serverType == SERVER_TYPES["DatabaseServer"]:
            from cloudbox.database.server.run import shutdown as dbShutdown
            dbShutdown(self)
        elif self.serverType == SERVER_TYPES["WorldServer"]:
            from cloudbox.world.run import shutdown as worldShutdown
            worldShutdown(self)