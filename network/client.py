import socket
import json
import threading
from tools import readObjects

class Client(threading.Thread):
  def __init__(self, host, port):
    threading.Thread.__init__(self, target=self.loop)
    self.hostport = (host, port)
    self.sock = None
    self.setup()

  def loop(self):
    self.sock = socket.socket()
    self.sock.connect(self.hostport)
    self.onConnect()
    for obj in readObjects(self.sock):
      self.onData(obj)
    self.onDisconnect()

  def send(self, obj):
    print("Sending", obj)
    self.sock.send(json.dumps(obj)+"\n")

  def setup(self):
    pass

  def onConnect(self):
    pass

  def onDisconnect(self):
    pass

  def onData(self, obj):
    pass



