import socket
import select
import errno
import time
import sys
import threading


def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))


HEADER_LENGTH = 10

IP = "127.0.0.1"

PORT = 2434
prCyan("------------------------------------------------")
my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

my_username = (f"[{my_username.lower()}]")

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

prCyan("------------------------------------------------")
prYellow(my_username + " has connected to the chatroom.")
prCyan("------------------------------------------------")

def sendMsg():
    message = input(f"{my_username} > ")
    # message = ""

    if message.lower() == 'quit' or message.lower() == 'exit' or message.lower() == 'disconnect' or message.lower() == 'dc' or message.lower() == 'leave':
        print("Exited")
        exit(1)

    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)


def recvMsg():
    try:
        while True:
            # receive stuff yk.
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Conncetion closed by the server")
                sys.exit()

            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            prGreen(username + " > " + message)
            # print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()

    except Exception as e:
        print('General Error', str(e))
        sys.exit()


def main():
    while True:
        recvMsg()
        sendMsg()


if __name__ == '__main__':
    main()