import etcd3

class ServerClient:
    def __init__(self):
        self.client = etcd3.client()

    def get_session(self):
        return self.client

    def update_character(self, playername, mapname, xcoord, ycoord, oldmapname=None):
        if(oldmapname):
            self.client.delete(f"/players/{mapname}/{playername}")

        self.client.replace(f"/players/{mapname}/{playername}/xcoord", "0", str(xcoord))
        self.client.replace(f"/players/{mapname}/{playername}/ycoord", "0", str(ycoord))
