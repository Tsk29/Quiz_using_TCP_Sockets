import socket
import select
from thread import *
import sys
import time
import random


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Setting up the server details and checks whether proper size of arguments are given
if len(sys.argv) != 2:
    print "Print in the following order : script, port number"
    exit()


Port = int(sys.argv[1])
player_number=int(input("Enter number of the players (minimum 2 players):"))
IP_address = socket.gethostbyname(socket.gethostname())

server.bind((IP_address, Port))
server.listen(100)

list_of_clients=[]


Q = [" The IETF standards documents are called ________: \n a.RFC b.RCF c.ID d.DFC",
     " A _________ set of rules that governs data communication.\n a.Protocols b.Standards c.RFCs d.Servers",
     " A __________ is a device that forwards packets between networks by processing the routing information included in the packet. \n a.bridge b.firewall c.router d.hub",
     " The number of layers in ISO OSI reference model is __________  \n a.5 b.7 c.6 d.10",
     " Application layer offers _______ service. \n a.End to end b.Process to process c.Both End to end and Process to process d.None of the mentioned",
      " The ____________ translates internet domain and host names to IP address. \n a.domain name system b.routing information protocol c.network time protocol d.internet relay chat",
     " The rfc of HTTP 1.1 is _______\n a.2610 b.2900 c.1930 d.2616",
   
     "  The Port no of HTTP  is _______\n a.80 b.25 c.84 d.69"]

A = ['a', 'a', 'c', 'b', 'a', 'a', 'd', 'a']

Count=[]
client = ["address",-1]
bzr =[0, 0, 0] #Buzzer List

def clientthread(conn, addr):
    conn.send("\n Hello !!!\n Welcome to this quiz!\n Answer any 5 questions correctly before your opponents do\n Press any key on the keyboard as a buzzer for the given question\n")
    
    while True:
            message = conn.recv(2048)
            if message:
                if bzr[0]==0:
                    client[0] = conn
                    bzr[0] = 1
                    i = 0
                    while i < len(list_of_clients):
                            if list_of_clients[i] == client[0]:
                                break
                            i +=1
                    client[1] = i

                elif bzr[0] ==1 and conn==client[0]:
                        bol = message[0] == A[bzr[2]][0]
                        print A[bzr[2]][0]
                        if bol:
                            broadcast("Player" + str(client[1]+1) + " :+1 Points" + "\n\n")
                            Count[i] += 1
                            if Count[i]==5:
                                broadcast("YOU  WON" + "\n")
                                end_quiz()
                                sys.exit()

                        else:
                            broadcast("Player" + str(client[1]+1) + ": -1 Points" + "\n\n")
                            Count[i] -= 1
                        bzr[0]=0
                        if len(Q) != 0:
                            Q.pop(bzr[2])
                            A.pop(bzr[2])
                        if len(Q)==0:
                            end_quiz()
                        quiz()

                else:
                        conn.send(" Player " + str(client[1]+1) + " pressed buzzer first\n\n")
            else:
                    remove(conn)

def broadcast(message):
    for clients in list_of_clients:
        try:
            clients.send(message)
        except:
            clients.close()
            remove(clients)
def end_quiz():
        broadcast("Game Over !!\n")
        bzr[1]=1
        i = Count.index(max(Count))
        broadcast("player " + str(i+1)+ " wins!! by scoring "+str(Count[i])+" points.")
        print("")
        for x in range(len(list_of_clients)):
            list_of_clients[x].send("You scored " + str(Count[x]) + " points.")
            
        server.close()


def quiz():
    bzr[2] = random.randint(0,10000)%len(Q)
    if len(Q) != 0:
        for connection in list_of_clients:
            connection.send(Q[bzr[2]])
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    Count.append(0)
    print addr[0] + " connected"
    start_new_thread(clientthread,(conn,addr))
    if(len(list_of_clients)==player_number):
        quiz()
conn.close()
server.close()
