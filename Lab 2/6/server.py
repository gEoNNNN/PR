import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
# start to listen for incoming connections
server.listen()

clients = []
nicknames = []


# send message to all clients connected
def broadcas(message):
    for client in clients:
        client.send(message)


# handle client
def handle(client):
    while True:
        try:  # try to receive a message and if it works, broadcast it
            message = client.recv(1024)  # bites basic method for a message
            broadcas(message)
        except:
            # remove client if something went wrong
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcas(f'{nickname} a parasit conversatia'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    print("Serverul a fost pornit")
    with open("file.txt", "r") as file:
        content = file.read()
        print(content)
    while True:
        # accept all the connections
        client, address = server.accept()
        print(f"Sa conectat cu adresa: {str(address)}")
        # first message will be the nickname
        # sent the key word to send the nickname to the server
        with open("file.txt", "a") as file:
            file.write(f'Nick\n')
        client.send('Nick'.encode('ascii'))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)
        print(f"Numele clientului este: {nickname}")
        broadcas(f'{nickname} sa alaturat conversatiei'.encode('ascii'))
        client.send('Te-ai alaturat conversatiei'.encode('ascii'))
        # cite un thread pentru fiecare user ca sa putem face mai multe operatii simultan
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()