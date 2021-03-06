# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import ServerFactory

from cloudbox.common.logger import Logger
from cloudbox.common.loops import LoopRegistry
from cloudbox.common.constants.classic import *
from cloudbox.common.constants.cpe import *
from cloudbox.hub.minecraft.handlers import classic, cpe
from cloudbox.hub.minecraft.protocol import MinecraftHubServerProtocol

class MinecraftHubServerFactory(ServerFactory):
    """
    I am the Minecraft side of the hub. I handle Minecraft client requests and pass them on to World Servers.
    """
    protocol = MinecraftHubServerProtocol

    def __init__(self, parentService):
        self.parentService = parentService
        self.clients = {}
        self.logger = Logger()
        self.loops = LoopRegistry()

    def startFactory(self):
        self.handlers = self.buildHandlers()

    def getWSFactoryInstance(self):
        return self.parentService.factories["WorldServerCommServerFactory"]

    def getServerType(self):
        return self.parentService.getServerType()

    def buildHandlers(self):
        handlers = {
            TYPE_INITIAL: classic.HandshakePacketHandler,
            TYPE_KEEPALIVE: classic.KeepAlivePacketHandler,
            TYPE_LEVELINIT: classic.LevelInitPacketHandler,
            TYPE_LEVELDATA: classic.LevelDataPacketHandler,
            TYPE_LEVELFINALIZE: classic.LevelFinalizePacketHandler,
            TYPE_BLOCKCHANGE: classic.BlockChangePacketHandler,
            TYPE_BLOCKSET: classic.BlockSetPacketHandler,
            TYPE_SPAWNPLAYER: classic.SpawnPlayerPacketHandler,
            TYPE_PLAYERPOS: classic.PlayerPosPacketHandler,
            TYPE_PLAYERORT: classic.PlayerOrtPacketHandler,
            TYPE_PLAYERDESPAWN: classic.PlayerDespawnPacketHandler,
            TYPE_MESSAGE: classic.MessagePacketHandler,
            TYPE_ERROR: classic.ErrorPacketHandler,
            TYPE_SETUSERTYPE: classic.SetUserTypePacketHandler,
        }
        if self.settings["main"]["enable-cpe"]:
            handlers.update({
                TYPE_EXTINFO: cpe.ExtInfoPacketHandler,
                TYPE_EXTENTRY: cpe.ExtInfoPacketHandler,
            })
        return handlers

    def claimID(self, proto):
        """
        Fetches ID for a client protocol instance.
        """
        for i in range(1, self.settings["main"]["max-clients"] + 1):
            if i not in self.clients:
                self.clients[i] = {"username": None, "protocol": proto}
                # TODO - Hook Call Here
                return i
        # Server is full
        return None

    def releaseID(self, clientID):
        del self.clients[clientID]

    ### World Server related functions ###

    def getWorldServersAvailability(self):
        statDict = {}
        for ws in self.wsFactory.worldServers:
            statDict[ws.id] = self.getWorldServerAvailability(ws.id)

    def getWorldServerAvailability(self, wsID):
        return self.wsFactory.worldServers[wsID].getStats()

    def relayMCPacketToWorldServer(self, packetID, packetData):
        pass

    def buildUsernameList(self, wsID=None):
        """
        Builds a list of {username: client object} by the client list, or
        specify a WorldServer ID to filter.
        """
        theList = dict()
        for cID, cEntry in self.clients.items():
            if cEntry["username"]:
                if wsID:
                    if cEntry["proto"].wsID == wsID:
                        theList[cEntry["username"].lower()] = cEntry["protocol"]
                else:
                    theList[cEntry["username"].lower()] = cEntry["protocol"]
        return theList

    def joinDefaultWorld(self, proto):
        """
        Joins the default world.
        """
        return
        mode = self.settings["main"]["entry-mode"]
        if mode == "solo":
            # Find out which WS has the default world and join it
            self.things
        elif mode == "distributed":
            # Find out which WS has the default world and join any of them.
            self.otherThings

    def joinWorldServer(self, proto, wsID):
        """
        Joins a World Server given its ID.
        """
        pass

    def leaveWorldServer(self, proto, wsID):
        """
        Leaves the current worldServer.
        """
        self.getWSFactoryInstance().leaveWorldServer(proto, wsID)

    def getBans(self, *args):
        """
        Fetches the ban information using the information given - username, IP, or both.
        """
        pass
