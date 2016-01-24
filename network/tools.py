import json

def readLines(socket):
    buff = ""
    while True:
        read = socket.recv(1024)
        if not read:
            return

        buff += read

        while "\n" in buff:
            line, buff = buff.split("\n", 1)
            yield line

def readObjects(socket):
    for line in readLines(socket):
        try:
            yield json.loads(line)
        except:
            print "EXCEPTION"
            import traceback
            traceback.print_exc()


