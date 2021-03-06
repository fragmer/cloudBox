# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from cloudbox.hub.heartbeat import HeartbeatService
from cloudbox.hub.minecraft.server import MinecraftHubServerFactory
from cloudbox.hub.world.server import WorldServerCommServerFactory


def init(serv):
    # Minecraft part of the Hub
    serv.factories["MinecraftHubServerFactory"] = MinecraftHubServerFactory(serv)
    # WorldServer part of the Hub
    serv.factories["WorldServerCommServerFactory"] = WorldServerCommServerFactory(serv)

    # Populate configuration.
    serv.loadConfig()
    serv.populateConfig()

    # Start up everything.
    TCP4ServerEndpoint(reactor, serv.settings["hub"]["main"]["ports"]["clients"])\
        .listen(serv.factories["MinecraftHubServerFactory"])
    TCP4ServerEndpoint(reactor, serv.settings["hub"]["main"]["ports"]["worldservers"])\
        .listen(serv.factories["WorldServerCommServerFactory"])

    # Heartbeat Service
    if serv.settings["hub"]["heartbeat"]["send-heartbeat"]:
        if serv.settings["hub"]["heartbeat"]["minecraft-heartbeat"]:
            serv.factories["HeartbeatService-Minecraft"] = HeartbeatService(serv,
                "http://minecraft.net/heartbeat.jsp").start()
        if serv.settings["hub"]["heartbeat"]["classicube-heartbeat"]:
            serv.factories["HeartbeatService-ClassiCube"] = HeartbeatService(serv,
                "http://www.classicube.net/server/heartbeat").start()

    reactor.run()

def stop(serv):
    reactor.stop()