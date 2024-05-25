import socket
from tkinter import *
from threading import Thread

def receive():
    while True:
        try:  # Put the try-except block inside the loop
            msg = s.recv(1024).decode("utf8")
            msg_list.insert(END, msg)  # Use END instead of tkinter.END
        except:
            print("There is an Error Receiving the Message")

def send():
    msg = my_msg.get()
    my_msg.set("")
    s.send(bytes(msg, "utf8"))
    if msg == "#quit":
        s.close()
        window.destroy()  # Use destroy() instead of close()

def on_closing():
    my_msg.set("#quit")
    send()

# Create the Tkinter window
window = Tk()
window.title("Chat Room Application")
window.configure(bg="green")

# Create the message frame
message_frame = Frame(window, height=100, width=100, bg="red")
message_frame.pack()

# Create the message listbox and scrollbar
my_msg = StringVar()
my_msg.set("")
scroll_bar = Scrollbar(message_frame)
msg_list = Listbox(message_frame, height=15, width=100, bg="red", yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
scroll_bar.config(command=msg_list.yview)
msg_list.config(yscrollcommand=scroll_bar.set)

# Create the label and entry field for the message input
label = Label(window, text="Enter the Message", fg='blue', font='Arial', bg='red')
label.pack()
entry_field = Entry(window, textvariable=my_msg, fg='red', width=50)
entry_field.pack()

# Create the send and quit buttons
send_button = Button(window, text="Send", font="Arial", fg='white', command=send)
send_button.pack()
quit_button = Button(window, text="Quit", font="Arial", fg='white', command=on_closing)
quit_button.pack()

# Connect to the server and start the receive thread
host = '127.0.0.1'
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
receive_thread = Thread(target=receive)
receive_thread.start()

# Start the Tkinter event loop
window.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window closing
mainloop()
