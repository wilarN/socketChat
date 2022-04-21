import socket
import select
import errno
import time
import sys
import threading
import os
from sys import platform


def prRed(skk): print("\033[91m {}\033[00m".format(skk))


def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


def prYellow(skk): print("\033[93m {}\033[00m".format(skk))


def prLightPurple(skk): print("\033[94m {}\033[00m".format(skk))


def prPurple(skk): print("\033[95m {}\033[00m".format(skk))


def prCyan(skk): print("\033[96m {}\033[00m".format(skk))


def prLightGray(skk): print("\033[97m {}\033[00m".format(skk))


def prBlack(skk): print("\033[98m {}\033[00m".format(skk))


HEADER_LENGTH = 10

IP = "127.0.0.1"

PORT = 2434


def logOutput(msg, logType):
    # Log
    if logType == 1:
        print("\n[ LOG ] " + msg)
    # Error
    elif logType == 2:
        print("\n[ ERROR ] " + msg)
    # Warning
    elif logType == 3:
        print("\n[ WARNING ] " + msg)


if platform == "linux":
    logOutput(msg="Using Linux", logType=1)

else:
    logOutput(msg="Using other OS than Linux", logType=1)


def outputPrint(lineBefore, msg, lineAfter):
    if platform == "linux":
        if lineBefore: prCyan("------------------------------------------------")
        prYellow(msg)
        if lineAfter: prCyan("------------------------------------------------")
    else:
        if lineBefore: print("------------------------------------------------")
        print(msg)
        if lineAfter: print("------------------------------------------------")


outputPrint(True, "", False)
my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

my_username = f"[{my_username.lower()}]"

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

outputPrint(True, f"{my_username} + has connected to the chatroom.", True)


def clearTerminal():
    clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    clearConsole()


def sendMsg():
    while True:
        message = input(f"{my_username} > ")
        # message = ""

        if message.lower() == 'quit' or message.lower() == 'exit' or message.lower() == 'disconnect' or message.lower() == 'dc' or message.lower() == 'leave':
            if os.name in ('nt', 'dos'):
                prRed("Left the chat.")
            else:
                print("Left the chat.")
            sys.exit()

        elif message.lower() == "help" or message.lower() == "/help":
            print("-----------"
                  " Help "
                  "-----------\n"
                  "- help(/help) --> Shows this help message.\n"
                  "- clear(/clear) --> Clear terminal.\n")

        elif message.lower() == "clear" or message.lower() == "/clear":
            clearTerminal()

        else:
            message = message.encode("utf-8")
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header + message)


def recvMsg():
    while True:
        try:
            while True:
                # receive stuff yk.
                username_header = client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    print("Connection closed by the server")
                    sys.exit()

                username_length = int(username_header.decode("utf-8").strip())
                username = client_socket.recv(username_length).decode("utf-8")

                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode("utf-8").strip())
                message = client_socket.recv(message_length).decode("utf-8")

                print("\n" + username + " > " + message, end="")
                print("\n" + f"{my_username} > ", end="")

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()

        except Exception as e:
            print('General Error', str(e))
            sys.exit()


t1 = threading.Thread(target=recvMsg, name="t1")
t2 = threading.Thread(target=sendMsg, name="t2")


def main():
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("threads closed.")


if __name__ == '__main__':
    main()
