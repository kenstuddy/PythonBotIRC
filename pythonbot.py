import socket
import sys

host = "irc.swiftirc.net"
port = 6667
nick = "pythonbot"
iden = "pythonbot"
rn = "pythonbot"
owner = "test2"
channel = "#mychannel"
buff = ''
clean = ''

s = socket.socket()
s.connect((host, port))

s.send(bytes("NICK %s\r\n" % nick, "UTF-8"))
s.send(bytes("USER %s %s nick :%s\r\n" % (iden, host, rn), "UTF-8"))
s.send(bytes("JOIN "+channel+"\r\n", "UTF-8"))

while 1:
    buff = s.recv(1024).decode("UTF-8")
    clean = buff.strip("\n\r")
    print(buff)
    if buff.find("PING :") != -1:
        s.send(bytes("PONG :ping\r\n", "UTF-8"))
        print("PONG :ping\r\n")
    # user authentication, 20 = max username length for swiftirc
    if buff.find("!say") != -1 and buff.find(owner, 1, 20) != -1:
        say_split = buff.split("!say ")
        s.send(bytes("PRIVMSG "+channel+" :"+say_split[1]+"\r\n", "UTF-8"))
        print("PRIVMSG "+channel+" :"+say_split[1]+"\r\n")
    if buff.find("!quit") != -1 and buff.find(owner, 1, 20) != -1:
        sys.exit()
