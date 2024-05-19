
import socket
import threading
import tkinter as tk

#client information
HOST = '127.0.0.5'
PORT = 26475  

#username
username = input("Enter your username: ")

#create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

#create GUI window
window = tk.Tk()
window.title(f"Chat App - {username}")

#message input field
message_input = tk.Entry(window, width=50)
message_input.pack()

#chat window
chat_window = tk.Text(window, height=20, width=70)
chat_window.pack()

#function to send messages
def send_message():
    message = message_input.get()
    message_input.delete(0, tk.END)

    #check if message is "quit"
    if message.lower() == "quit":
        client_socket.sendall("quit".encode("utf-8"))
        window.destroy()  # Close the chat window
    else:
        client_socket.sendall(f"{username}: {message}".encode("utf-8"))


#function to receive messages
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                chat_window.insert(tk.END, f"{message}\n")
        except:
            break

#send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

#start message receiving thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

#run the main loop
window.mainloop()

#close socket when finished
client_socket.close()
