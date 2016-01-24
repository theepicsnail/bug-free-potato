# python -m chat/client
from network.client import Client

class ChatClient(Client):
  def onConnect(self):
    self.send({"Message": "Hooray"})
  def onDisconnect(self):
    print "Disconnected"
  def onData(self, data):
    print "Data:", data

client = ChatClient("theepicsnail.net", 1234)
client.start()
while True:
    client.send({"Message":raw_input()})
