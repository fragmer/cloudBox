# cloudBox - Minecraft Classic of the Cloud.

cloudBox is a solution for putting Minecraft Classic on the cloud, based on Twisted. It works by separating workloads from one single server to different servers. It is designed to be fast, efficient and powerful.

cloudBox is currently under heavy development. To contact the developer, drop by #cloudbox at one of the following IRC networks: EsperNet (main channel), Freenode, StormBit, ArchivesMC.

# Server Overview

## Hub Server

The Hub Server handles communication between Minecraft Clients and World Servers, and act as a proxy between the clients and the World Servers. It maintains connection between all servers, such as the World Server, the Database Server, and the Logger Server. It also operates an API that websites can query from.

## World Server

The World Server hosts the actual world files. Aside from handling clients, the World Server is also equipped with a physics engine and a world generator. The World Server also handles commands. The architecture allows multiple World Servers to be run.

## Database Server

The Database Server handles communication between other servers and the database, providing an abstraction layer between a DBMS and the servers.

## Web Server

The Web server provides the website front-end to the server, allowing users to change settings of their worlds. This server is optional.

# What makes cloudBox special

## Feature-rich

cloudBox has a lot of features that other server softwares do not have: These include user scripting, a robust web interface, distributed realm mode, chat channels, while having basic features of a modern server, such as ranks, /blb (/cuboid) and world manipulation tools, etc. It also supports OpenClassic clients.

## High-Performance

cloudBox is designed to hold hundreds or even thousands of people with ease. As it is designed to allow horizonal scaling, more World Servers can be added to handle extra traffic easily. All Servers also employ caching, such as memcached, to decrease query amounts and speed up performance. World Servers "juggle" world files under the guidance of the Hub Server to maintain balance between World Servers.

## Flexibility

The configuration file is easy to nagivate while proving a lot of options to fine-tune the system. cloudBox is designed to be horizontally scaled - you can add as many World Servers as you want to balance the load. The ranks system most users use have been upgraded to a usergroup system, where server admins can select commands users in the usergroup can run, along with other settings.

## Extensibility

Every Server is equipped with a plugin system that can be used to extend the features of servers. The powerful hooking system will allow you to hook into almost everywhere of the server.

## Security

World Servers cannot be accessed directly. The API can be configured to only allow selective IPs to query information from.

# Development status

cloudBox is currently under heavy developement, and there are no ETA at the moment. A first preview should be up when the skeleton is done, though.

# Contribution

cloudBox is currently only a summer project for me, so if you're interested your help is greatly apperciated. Please drop by our IRC channel if you wish to know more about how to contribute.

# More to come...