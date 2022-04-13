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
    chatFrame = ttk.LabelFrame(root, text="Main Chatroom", width=height, height=width)
    # chatFrame.place(x=int(width)/2, y=int(height)/2)
    chatFrame.place(x=0, y=0)


button = ttk.Button(root, text="Join Chatroom", style="Accentbutton", command=mainChatFunction)
style.configure("Accentbutton", foreground="black")

# Packing
button.pack()
root.mainloop()

