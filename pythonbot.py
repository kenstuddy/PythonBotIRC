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
# Create the socket for the IRC connection.
s = socket.socket()
# Connect to the hostname (DNS) and port (6667 is the default IRC port)
s.connect((host, port))

# Send the NICK to the socket which tells the IRCD (IRC Daemon) to set our nick
# IRC usually uses UTF-8, so we specify UTF-8 as the character encoding.
# The socket sends the bytes and the IRCD handles it as it is UTF-8 encoded.
s.send(bytes("NICK %s\r\n" % nick, "UTF-8"))
# Send the user to the socket
s.send(bytes("USER %s %s nick :%s\r\n" % (iden, host, rn), "UTF-8"))
# Send the JOIN message to the socket to join the channel we specified
s.send(bytes("JOIN "+channel+"\r\n", "UTF-8"))

while 1:
    # Here we decode the socket into a readable line of text
    buff = s.recv(1024).decode("UTF-8")
    # Here we strip the new line and carriage return
    clean = buff.strip("\n\r")
    # Here we print the new line to the console
    print(clean)
    # Here we check if the server has sent a PING, and make sure it is
    # actually from the server, and not in a channel/private message
    if buff.find("PING :") != -1 and buff.find("PRIVMSG") == -1:
        s.send(bytes("PONG :ping\r\n", "UTF-8"))
        print("PONG :ping\r\n")
    # Here is user authentication, 20 = max username length for swiftirc
    if buff.find("!say") != -1 and buff.find(owner, 1, 20) != -1:
        # Here we split to extract what the bot has to say
        say_split = buff.split("!say ")
        # Here we send what the bot has to say as a private message
        s.send(bytes("PRIVMSG "+channel+" :"+say_split[1]+"\r\n", "UTF-8"))
        print("PRIVMSG "+channel+" :"+say_split[1]+"\r\n")
    # Here is quitting out of the program, again with user authentication
    if buff.find("!quit") != -1 and buff.find(owner, 1, 20) != -1:
        # Here we exit the program using the exit function in the sys module
        sys.exit()
