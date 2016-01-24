import socket
import json
import threading

def readlines(socket):
    """Read a socket and yield each line without the \n"""
    buff = ""
    while True:
        read = socket.recv(1024)

        if not read:
            return

        buff += read
        while "\n" in buff:
            line, buff = buff.split("\n", 1)
            yield line


class Client(threading.Thread):
    """Each client that's connected to the server

    send({"name":"snail", "message":"whatever"})
    or
    send([1,2,3])
    etc.. anything that's jsonable

    this will call onClientData(client, object) with the
    deserialized json object
    """

    def __init__(self, server, connection):
        threading.Thread.__init__(self, target=self.loop)
        self.connection = connection
        self.server = server
        self.name = str(self.connection.getpeername())

    def loop(self):
        self.server.addClient(self)
        for line in readlines(self.connection):
            try:
                obj = json.loads(line)
                self.server.handleClientData(self, obj)
            except:
                print "EXCEPTION", self
                print "Line:", line
                import traceback
                traceback.print_exc()

        self.server.removeClient(self)

    def send(self, obj):
        try:
            self.connection.send(json.dumps(obj) + "\n")
        except:
            self.server.removeClient(self)

    def __str__(self):
        return self.name



class Server(threading.Thread):

    def __init__(self, port):
        threading.Thread.__init__(self, target=self.__loop__)
        self.port =port
        self.clients = []
        self.setup()

    def __loop__(self):
        self.server = socket.socket()
        self.server.bind(('', self.port))
        self.server.listen(5)
        while True:
          connection, address = self.server.accept()

          Client(self, connection).start()

    def addClient(self, client):
        self.clients.append(client)
        self.onClientAdd(client)

    def removeClient(self,client):
        self.clients.remove(client)
        self.onClientRemove(client)

    def handleClientData(self, client, line):
        self.onClientData(client, line)


    # Things below here, subclasses should use/implement
    def setup(self):
        pass
    def onClientAdd(self, client):
        pass
    def onClientData(self, client, data):
        pass
    def onClientRemove(self, client):
        pass

    # Use this to annouce to everyone (except clients in skip)
    def broadcast(self, obj, skip=[]):
        if type(skip) != list:
            skip = [skip]

        for client in self.clients:
            if client in skip:
                continue

            client.send(obj)

