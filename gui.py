import tkinter as tk
import tkinter.scrolledtext
import tkinter.ttk as ttk
import threading
import socket

HEADER_LENGTH = 10

IP = "127.0.0.1"

PORT = 2434

###ENTER USERNAME HERE

username = "testUser"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)


root = tk.Tk()

height = "400"
width = "300"


root.title("Chatroom")
root.geometry(f"{height}x{width}")
root.resizable(width=False, height=False)
style = ttk.Style(root)
root.tk.call('source', 'guiStuff/azure.tcl')
style.theme_use('azure')
style.configure("Accentbutton", foreground="black")


def removeWidget(widget):
    widget.pack_forget()


def mainChatFunction():
    removeWidget(button)
    removeWidget(label1)
    chatFrame = ttk.LabelFrame(root, text="Main Chatroom", width=height, height=width)
    chatFrame.place(x=0, y=0)
    chatTextEnter = ttk.Entry(root)
    chatTextEnter.place(x=20, y=260)
    chatArea = tkinter.scrolledtext.ScrolledText(root)
    chatArea.pack(padx=20, pady=20)
    chatArea.configure(state='disabled')

    def sendMessage():
        message = f"{username}: {chatTextEnter.get()}"
        client_socket.send(message.encode('utf-8'))


    sendButton = ttk.Button(root, text="Send", style="Accentbutton", command=sendMessage)
    sendButton.place(x=250, y=260)


button = ttk.Button(root, text="Join Chatroom", style="Accentbutton", command=mainChatFunction)
label1 = ttk.Label(root, text="Press to join the main chatroom")


# Packing
button.pack()
label1.pack()
root.mainloop()
