# python -m chat/client
import threading
from network.client import Client
from itertools import product
import pygame
pygame.init()

COLORS = list(product(*[(0,255)]*3))

class Window(threading.Thread):
  def __init__(self, client):
    threading.Thread.__init__(self, target=self.eventloop)

    self.client = client
    self.display = pygame.display.set_mode((500,500))
    self.paletteSize = 500/len(COLORS)
    self.display.fill((255,255,255))
    self.drawOverlay()
    self.color = COLORS[0]
    self.start()

  def eventloop(self):
    start = None
    while True:
      evt = pygame.event.poll()
      if evt.type == pygame.QUIT:
        pygame.quit()
        return

      if evt.type == pygame.MOUSEBUTTONDOWN:
        start = evt.pos
        color = self.selectColor(start)
        if color is not None:
          print color
          start = None
          self.color = color
        continue

      if evt.type == pygame.MOUSEBUTTONUP:
        if start:
          # This dict needs to match the self.line method
          client.send({"type":"line", "start": start, "end":evt.pos, "color":self.color, "size":5})
        start = None

  def selectColor(self, pos):
    print pos
    if pos[1] > self.paletteSize:
      return None
    i = pos[0] / self.paletteSize
    if 0<= i < len(COLORS):
        return COLORS[i]
    return None

  def drawOverlay(self):
    for i, color in enumerate(COLORS):
      x = i * self.paletteSize
      pygame.draw.rect(self.display, color, [x, 0, x + self.paletteSize, self.paletteSize])
    pygame.display.flip()

  def line(self, start, end, color, size):
      print self.line
      pygame.draw.line(self.display, color, start, end, size)
      self.drawOverlay()

class ChatClient(Client):

  def setup(self):
    self.window = Window(self)

  def onConnect(self):
    pass

  def onDisconnect(self):
    pass

  def onData(self, data):
    if "type" not in data:
      return

    msgType = data["type"]
    del data["type"]
    if msgType == "line":
      self.window.line(**data)


client = ChatClient("theepicsnail.net", 1234)
client.start()
while True:
    client.send({"Message":raw_input()})
