# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from zope.interface import Interface, Attribute


class IPacketHandler(Interface):
    """
    Interface for all DataHandlers.
    """

    parent = Attribute("The parent the DataHandler belongs to.")

    def handleData(data):
        """
        Acts upon data.
        """

    def packData(data):
        """
        Packs the data to the desired wire-transfer format.
        """

    def feed(data):
        """
        Feeds data to the internal buffer.
        """

class IGeneralPacketProcessor(Interface):
    """
    Interface for all GeneralPacketProcessors.
    """
    buffer = Attribute("""Buffer for data received.""")
    handlers = Attribute("""Handlers for specific packet types received.""")
    parent = Attribute("""Parent instance.""")

    def init(parent, handlers, buffer):
        """
        Initializes the GPP.
         handlers: A dict of the format {packetTypeID: [ParsingHandler, DataHandler]}
        parent: The parent that is using the parser.
        buffer:; The buffer string.
        """

    def parseFirstPacket():
        """
        Parses the first packet in the buffer.
        """

    def packPacket(handler, data):
        """
        Packs a packet using the given handler.
        """

    def _populateBaseVariables():
        """
        Populates base variables to pass to handlers.
        """

class ILoopRegistry(Interface):
    """
    Interface for a Loop Registry.
    """

    loops = Attribute("The dictionary that contains all the loops.")

    def registerLoop(name, obj):
        """
        Registers a loop.
        """

    def unregisterLoop(name):
        """
        Unregisters a loop.
        """