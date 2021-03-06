# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet.protocol import Protocol

from cloudbox.common.gpp import MSGPackPacketProcessor


class WorldServerCommServerProtocol(Protocol):
    """
    The protocol class for the WorldServer communicator factory.
    """

    def __init__(self):
        self.wsID = None

    def getServerType(self):
        return self.factory.getServerType

    def connectionMade(self):
        """
        Triggered when connection is established.
        """
        self.gpp = MSGPackPacketProcessor(self, self.factory.handlers)

    def dataReceived(self, data):
        """
        Triggered when data is received.
        """
        # Pass on the data to the GPP
        # First, add the data we got onto our internal buffer
        self.gpp.feed(data)
        # Ask the GPP to decode the data, if possible
        self.gpp.parseFirstPacket()

    ### World Server related functions ###

    def getStats(self):
        # TODO
        return {
            "players": 0
        }

    ### End-client related functions ###

    def protoDoJoinServer(self, proto):
        """
        Makes the protocol join the server.
        """
        pass

    def protoDoLeaveServer(self, proto):
        """
        Makes the protocol leave the server.
        """
        pass