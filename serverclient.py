import time

import etcd3


class OnlinePlayer:
    def __init__(self, playername, coordinates, moving, facing):
        self.name = playername
        self.coordinates = coordinates
        self.moving = moving
        self.facing = facing
        self.ping = time.time()


class ServerClient:
    def __init__(self, playername):
        self.client = etcd3.client()
        self.name = playername

    def get_session(self):
        return self.client

    def init_character(self, mapname, xcoord, ycoord, facing=0, moving=False):
        self.client.put(f"/players/{mapname}/{self.name}", "playername")

        self.client.put(f"/players/{mapname}/{self.name}/xcoord", str(xcoord))
        self.client.put(f"/players/{mapname}/{self.name}/ycoord", str(ycoord))
        self.client.put(f"/players/{mapname}/{self.name}/facing", str(facing))
        self.client.put(f"/players/{mapname}/{self.name}/moving", str(moving))
        self.client.put(f"/players/{mapname}/{self.name}/ping", str(time.time()))

    def update_character(
        self, mapname, xcoord, ycoord, facing, moving, oldmapname=None
    ):
        if oldmapname:
            self.client.delete(f"/players/{mapname}/{self.name}")
            self.client.put(f"/players/{mapname}/{self.name}", "playername")

        self.client.put(f"/players/{mapname}/{self.name}/xcoord", str(xcoord))
        self.client.put(f"/players/{mapname}/{self.name}/ycoord", str(ycoord))
        self.client.put(f"/players/{mapname}/{self.name}/facing", str(facing))
        self.client.put(f"/players/{mapname}/{self.name}/moving", str(moving))
        self.client.put(f"/players/{mapname}/{self.name}/ping", str(time.time()))

    def get_players_in_map(self, mapname):
        rawdata = self.client.get_prefix(f"/players/{mapname}/")
        playerlist = []
        for key in rawdata:
            if key[0].decode("utf-8") != "playername":
                continue

            playername = key[1].key.decode("utf-8").split("/")[3]
            if str(self.name) == str(playername):
                continue

            player = {"name": playername}
            playerrawinfo = self.client.get_prefix(f"/players/{mapname}/{playername}/")

            for inforaw in playerrawinfo:
                key = inforaw[1].key.decode("utf-8").split("/")[4]
                value = inforaw[0].decode("utf-8")
                player[key] = value
            playerlist.append(player)
        return playerlist
