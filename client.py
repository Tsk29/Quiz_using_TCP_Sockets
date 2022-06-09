
import socket
import select
import sys


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 2:
    print "Print in the following order : script, port number"
    exit()


Port = int(sys.argv[1])

IP_address = socket.gethostbyname(socket.gethostname())

server.connect((IP_address, Port))


while True:

   
    sockets_list = [sys.stdin, server]

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print message
        else:
            message = sys.stdin.readline()
            server.send(message)
            sys.stdout.flush()
server.close()
sys.exit()
