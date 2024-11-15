import socket
import threading
import random
import time

# Lock and Condition variable to control access and coordination between threads
file_lock = threading.Lock()
write_condition = threading.Condition()

# File name to be used by threads
file_name = 'shared_file.txt'

# Variable to track if a write operation is happening
write_in_progress = False

def handle_client(client_socket, client_address):
    """Handles the incoming client requests."""
    print(f"New connection from {client_address}")
    with client_socket:
        while True:
            try:
                data = client_socket.recv(1024).decode()  # Receive data from client

                if not data:  # If no data, close the connection
                    break

                # Command parsing (simplified)
                if data.startswith("write:"):
                    message = data[6:]  # Everything after "write:"
                    # Process the write request in a separate thread
                    threading.Thread(target=handle_write, args=(message, client_socket)).start()
                    client_socket.sendall(f"Message received for writing: {message}".encode())
                elif data == "read":
                    # Process the read request in a separate thread, but read must wait for write to finish
                    threading.Thread(target=handle_read, args=(client_socket,)).start()
                else:
                    client_socket.sendall("Invalid command".encode())

            except Exception as e:
                print(f"Error handling client {client_address}: {e}")
                break

def handle_write(message, client_socket):
    """Write to the shared file with thread safety and coordination."""
    global write_in_progress

    # Wait for any ongoing reads to finish before starting the write operation
    with write_condition:
        # If there's an ongoing write operation, wait until it's done
        while write_in_progress:
            write_condition.wait()

        # Mark that a write operation is in progress
        write_in_progress = True

    sleep_time = random.randint(1, 7)  # Random sleep time between 1 to 7 seconds
    print(f"Server is sleeping for {sleep_time} seconds before writing: {message}")
    time.sleep(sleep_time)  # Sleep for a random time before writing

    with file_lock:  # Locking the file for thread-safe write
        with open(file_name, 'a') as file:
            file.write(message + '\n')
            print(f"Written to file: {message}")

    # Once the write is done, mark it as completed and notify waiting threads
    with write_condition:
        write_in_progress = False
        write_condition.notify_all()  # Notify all waiting threads (if any)

def handle_read(client_socket):
    """Read from the shared file with thread safety, ensuring write completion first."""
    global write_in_progress

    # Wait for all write operations to complete before starting to read
    with write_condition:
        # If there's an ongoing write operation, wait until it's done
        while write_in_progress:
            print("Read operation is waiting for write operation to finish.")
            write_condition.wait()

    sleep_time = random.randint(1, 7)  # Random sleep time between 1 to 7 seconds
    print(f"Server is sleeping for {sleep_time} seconds before reading from file.")
    time.sleep(sleep_time)  # Sleep for a random time before reading

    with file_lock:  # Locking the file for thread-safe read
        try:
            with open(file_name, 'r') as file:
                content = file.read()
            print("Read from file:", content)
            client_socket.sendall(content.encode())
        except FileNotFoundError:
            client_socket.sendall("File not found.".encode())

def start_server(host='127.0.0.1', port=65432):
    """Start the server to accept client connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server started, listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == '__main__':
    start_server()
