# import necessary libreries
import socket
import threading #helps to work at the OS level

# establish server
host = '127.0.0.1'
port = 44444
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# list of clients with username
clients = list()
username = list()

# remove explicit words
def open_file():
    try:
        fhand = open('D:\Projects\Python Chatroom\language.txt')
        return fhand
    except:
        print('Language file not found')

def close_file(fhand):
    if fhand != None:
        fhand.close()

def change(word):
    if len(word) <= 1:
        return '*'
    res = word[0]
    for i in range(len(word)-2):
        res += '*'
    res += word[-1]
    return res

def clean(message):
    #find alternative for explicit word
    fhand = open_file()
    if fhand == None:
        return message
    lang = fhand.read().split('\n')
    close_file(fhand)
    message = message.split(' ')
    for word in message:
        if word in lang:
            message[message.index(word)] = change(word)

    res = ""
    for word in message:
        res += word + " "
    print(res)
    return res

# broadcast message to all clients
def broadcast(message,sender = None):
    for client in clients:
        if sender == None or sender != client:
            client.send(message)

# recieve message from client. If any error is occured remove client
def read(client):
    while True:
        try:
            message = client.recv(1024)
            message = clean(message.decode('ascii').rstrip())
            broadcast(message.encode('ascii'), client)
        except:
            client.close()
            index = clients.index(client)
            clients.remove(client)
            broadcast("{} left the chatroom".format(username[index]).encode('ascii'))
            print("{} left the chatroom".format(username[index]))
            username.remove(username[index])
            break

# respond to connection request from clients and start a separate thread for it
def connect():
    while True:
        client, address = server.accept()
        client.send("Enter username: ".encode('ascii'))
        client_username = client.recv(1024).decode('ascii')
        broadcast("{} Joined".format(client_username).encode("ascii"))
        print("{} connected as {}".format(address, client_username))
        clients.append(client)
        username.append(client_username)
        thread = threading.Thread(target = read, args = (client, ))
        thread.start()

#call function connect
connect()

        
