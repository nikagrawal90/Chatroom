#importing required libraries
import socket
import threading

# server address
port = 44444
server = '127.0.0.1'

#prompt for username
username = input('Enter your username: ')

# connect with server
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server, port))
except:
    print("Error connecting to Server!")

# receive messages
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'Enter username: ':
                client.send(username.encode('ascii'))
            else :
                print(message)
        except:
            print('Error retrieving message!')
            client.close()
            break


# send message
def send():
    while True:
        try:
            message = "{}: {}".format(username, input(''))
            client.send(message.encode('ascii'))
        except:
            print('Error sending message')

#start separate threads to receive and send messages
thread_receive = threading.Thread(target = receive)
thread_send = threading.Thread(target = send)

thread_receive.start()
thread_send.start()
    
        
