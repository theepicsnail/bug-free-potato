#python -m pong/server
from network.server import Server
from random import random
from math import cos, sin, pi


class PongServer(Server):
    def setup(self):
        self.player1 = None
        self.player2 = None
        self.ball = {"x":0, "y":0, "dx":0, "dy":0}

    def onClientAdd(self, client):
        if self.player1 is None:
            self.player1 = client
        elif self.player2 is None:
            self.player2 = client
            self.spawnBall()

    def spawnBall(self):

        # random from -pi/4 to pi/4
        angle = -pi/4 + (pi/2) * random()
        if random() > .5:
            # 50% make it from
            # 3/4pi to 5/4pi
            angle += pi


        self.broadcast({
           "type":"ball",
           "x": .5,
           "y": random()*.8+.1 # .1 to .9
           "dx": v * cos(angle),
           "dy": v * sin(angle)})

    def onClientRemove(self, client):
        self.broadcast({
          "Message": "%s has left" % client})
    def onClientData(self, client, data):
        message = "%s: %s" % (client, data["Message"])
        self.broadcast({"Message": message})

pong = PongServer(1234)
try:
    pong.run()
except:
    print "Shutting down"
    for client in pong.clients:
        client.connection.close()
    chat.broadcast("")
