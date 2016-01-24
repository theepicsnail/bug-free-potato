from Tkinter import *
from ScrolledText import ScrolledText
import random
import socket

class Window:
    def __init__(self):
        root = Tk()
        root.title("pygame")
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=10)

        chat = ScrolledText(root)
        chat.grid(columnspan=2, sticky=E+W)

        entryvar = StringVar()
        entry = Entry(root, textvariable=entryvar)
        entry.grid(column=1, row=1, sticky=E+W)

        namevar = StringVar()
        name = Entry(root, textvariable=namevar)
        name.grid(column=0, row=1, sticky=E+W)

        namevar.set("User%s" % random.randint(1000,10000))
        entry.focus()

        self.root = root
        self.chat = chat

    def run(self):
        self.root.mainloop()

    def addMessage(self, message):
        self.chat.config(state=NORMAL)
        self.chat.insert(END, "---\n")
        self.chat.insert(END, message + "\n")
        self.chat.config(state=DISABLED)

class Network:
    def __init__(self):
        self.s = socket.socket()

    def run(self):
        self.s.bind(("theepicsnail.net", 1234))

w = Window()

for i in range(100):
    w.addMessage("X" * i)
w.run()
