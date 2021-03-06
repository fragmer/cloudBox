# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, connectionDone as _connDone

from cloudbox.common.constants.classic import *
from cloudbox.common.gpp import MinecraftClassicPacketProcessor
from cloudbox.common.logger import Logger
from cloudbox.common.loops import LoopRegistry

class MinecraftHubServerProtocol(Protocol):
    """
    Main protocol class for communicating with clients.
    """

    ### Twisted Methods ###

    def connectionMade(self):
        """
        Called when a connection is made.
        """
        self.id = None
        self.username = None
        self.wsID = None  # World Server this user belongs to
        self.identified = False
        self.state = {}  # A special dict used to hold temporary "signals"
        self.logger = Logger()
        self.loops = LoopRegistry()
        # Get an ID for ourselves
        self.id = self.factory.claimID(self)
        if self.id is None:
            self.sendError("The server is full.")
            return
        self.ip = self.transport.getPeer().host
        self.gpp = MinecraftClassicPacketProcessor(self, self.factory.handlers)

    def connectionLost(self, reason=_connDone):
        # Leave the world
        self.factory.leaveWorldServer(self, self.wsID)
        # Release our ID
        self.factory.releaseID(self.id)

    def dataReceived(self, data):
        """
        Called when data is received.
        """
        # Add the data we got onto our internal buffer
        self.gpp.feed(data)
        self.logger.debug(data)
        self.gpp.parseFirstPacket()

    def getServerType(self):
        return self.factory.getServerType()

    ### Message Handling ###

    def send(self, msg):
        """
        Sends raw data to the client.
        """
        self.transport.write(msg)

    def sendPacket(self, packetId, packetData):
        finalPacket = self.factory.handlers[packetId].packData(packetData)
        self.transport.write(chr(packetId) + finalPacket)
        self.logger.debug(finalPacket)

    def sendError(self, error, disconnectNow=False):
        """
        Sends an error the client.
        """
        self.factory.logger.info("Sending error: %s" % error)
        self.sendPacket(TYPE_ERROR, {"error": error})
        if disconnectNow:
            self.transport.loseConnection()
        else:
            reactor.callLater(0.2, self.transport.loseConnection)

    def sendMessage(self, message):
        """
        Sends a message to the client.
        """
        self.sendPacket(TYPE_MESSAGE, {"message": message})

    def sendKeepAlive(self):
        """
        Sends a ping to the client.
        """
        self.sendPacket(TYPE_KEEPALIVE, {})

    def sendBlock(self, x, y, z, block=None):
        """
        Sends a block.
        """
        if block is not None:
            self.sendPacket(TYPE_BLOCKSET, {"x": x, "y": y, "z": z, "block": block})
        else:
            # Ask the World Server to get the block, and send it.
            # TODO
            return

    ### Relay functions ###
    def relayClientData(self):
        pass