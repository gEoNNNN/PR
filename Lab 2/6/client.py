import socket
import threading

nickname = input("Introduce un nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive():
    with open("file.txt", "r") as file:
        content = file.read()
        print(content)
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'Nick':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("A aparut o eroare")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}:{input("")}'
        with open("file.txt", "a") as file:
            if message != 'Nick':
                file.write(f'{message}\n')
        client.send(message.encode("ascii"))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()