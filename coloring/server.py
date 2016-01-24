from network.server import Server

class Server(Server):

    def onClientAdd(self, client):
        self.broadcast({
          "Message": "%s has joined" % client})
    def onClientRemove(self, client):
        self.broadcast({
          "Message": "%s has left" % client})
    def onClientData(self, client, data):
        message = "%s: %s" % (client, data["Message"])
        self.broadcast({"Message": message})

chat = ChatServer(1234)
try:
    chat.run() # Run in the current thread instead of start()ing in another
except:
    print "Shutting down"
    for client in chat.clients:
        client.connection.close()
    chat.broadcast("")
