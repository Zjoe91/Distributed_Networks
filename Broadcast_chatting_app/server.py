import socket
import threading
import tkinter as tk

#server information
HOST = '127.0.0.5'
PORT = 26475  

#client list
clients = []

#function to handle incoming messages
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")

            #broadcast message if not "quit"
            if message and message.lower() != "quit":
                for client in clients:
                    if client != client_socket:
                        client.sendall(message.encode("utf-8"))

            #remove client if "quit"
            elif message.lower() == "quit":
                clients.remove(client_socket)
                client_socket.close()
                print(f"Client {address} disconnected with 'quit' command.")
                break

        except:
            #handle other exceptions
            clients.remove(client_socket)
            client_socket.close()
            break


#create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

#start accepting connections
while True:
    client_socket, address = server_socket.accept()
    print(f"Client connected from {address}")

    #add client to list and create thread
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

#close server socket when finished
server_socket.close()
