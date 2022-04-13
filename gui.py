import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()

height = "400"
width = "300"

root.title("Chatroom")
root.geometry(f"{height}x{width}")
root.resizable(width=False, height=False)
style = ttk.Style(root)
root.tk.call('source', 'guiStuff/azure.tcl')
style.theme_use('azure')


def removeWidget(widget):
    widget.pack_forget()


def mainChatFunction():
    removeWidget(button)
    removeWidget(label1)
    chatFrame = ttk.LabelFrame(root, text="Main Chatroom", width=height, height=width)
    chatFrame.place(x=0, y=0)
    chatTextEnter = ttk.Entry(root)
    chatTextEnter.place(x=20, y=260)


button = ttk.Button(root, text="Join Chatroom", style="Accentbutton", command=mainChatFunction)
label1 = ttk.Label(root, text="Press to join the main chatroom")
style.configure("Accentbutton", foreground="black")

# Packing
button.pack()
label1.pack()
root.mainloop()

