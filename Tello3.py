# 7/10/2019
import threading
import socket
import sys
import math
import time
# 10.0.0.16
# 192.168.10.2
host = '192.168.10.4'
port = 8888
locaddr = (host, port)
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)

sock.bind(locaddr)

go = ["OK"]

def recv():
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
            if data.decode(encoding="utf-8") == "OK" or "ok":
                go[0] = "go"
            else:
                go[0] = "error"
                print(data.decode(encoding="utf-8"))

        except Exception:
            print('\nExit . . .\n')
            break


# recvThread create
threading.Thread(target=recv).start()

print("Hi Edward!")

test = int(math.sin(math.radians(60))*100)

command_list = [
                "go 500 0 0 100"
                ]

command_list2 = ["command",
                 "curve 100 50 0 200 0 0 50",
                 "land"]

while True:

    try:
        msg = input("")


        if "cmd" in msg:
            sock.sendto("command".encode(encoding="utf-8"), tello_address)
            print("I am at your service")
        elif "btr" in msg:
            sock.sendto("battery?".encode(encoding="utf-8"), tello_address)
        elif "land" in msg:
            sock.sendto("land".encode(encoding="utf-8"), tello_address)

        else:
            if "go" in msg:
                time.sleep(2)
                for i in range(0, len(command_list)):
                    sock.sendto(command_list[i].encode(encoding="utf-8"), tello_address)
                    print(command_list[i])
                    timer = 0
                    while go[0] != "go":
                        time.sleep(.1)
                        timer += .1
                        if timer >= 10:
                            print("reached" + str(timer))

                            break
                    go[0] = "not received"
                    time.sleep(.1)
                    if timer >= 10:
                        break

    except KeyboardInterrupt:
        print('\n . . .\n')
        sock.close()
        break
