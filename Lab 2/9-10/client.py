import socket
import random
import time


def start_client(host='127.0.0.1', port=65432):
    """Start the client to send commands to the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        while True:
            command = input("Enter command (write:<message> or read, type 'exit' to quit): ")
            if command.lower() == 'exit':
                break

            # Send the command to the server
            client_socket.sendall(command.encode())

            if command.startswith("write:"):
                # Sleep for 1-7 seconds after writing a message
                sleep_time = random.randint(1, 7)
                print(f"Sleeping for {sleep_time} seconds after write command.")
                time.sleep(sleep_time)  # Sleep for the random time

            # Receive the server's response
            response = client_socket.recv(1024).decode()
            print(f"Server response: {response}")


if __name__ == '__main__':
    start_client()
