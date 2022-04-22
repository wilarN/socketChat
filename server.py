import socket
import select
import sys
import time
import threading
import os

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 2434

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}

serverActive = False

# ANNOUNCEMENT
msg = "Welcome to this epic chatroom."
msg = f'{len(msg):<{HEADER_LENGTH}}' + msg

def log_to_file(text_to_log):
    # Log connections etc to external logfile.
    pass

def clearTerminal():
    clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    clearConsole()

    '''
    global clearstuff
    if sys.platform.startswith('linux'):
        clearstuff = lambda: os.system('clear')

    elif sys.platform.startswith('win32'):
        clearstuff = lambda: os.system('cls')

    elif sys.platform.startswith('freebsd'):
        clearstuff = lambda: os.system('clear')
    else:
        print("Cannot clear terminal on this system yet.")
    '''


def send_command():
    global serverActive
    while serverActive:
        while True:
            command = input("Server > ")
            # command = ""

            if command.lower() == "help" or command.lower() == "/help":
                print("-----------"
                      " Help "
                      "-----------\n"
                      "- help(/help) --> Shows this help message.\n"
                      "- kick(/kick) --> Kick a user.\n"
                      "- ban(/ban) --> Ban a user.\n"
                      "- stop(/stop) // kill(/kill) // exit(/exit) --> Stop server.\n"
                      "- all(/all) --> Announcement to all users.\n"
                      "- ip(/ip) --> Get IP of a user.\n"
                      "- clear(/clear) --> Clear terminal.\n")
            # kick
            elif command.lower() == "kick" or command.lower() == "/kick":
                print("Kick someone.")
            # ban
            elif command.lower() == "ban" or command.lower() == "/ban":
                print("Ban someone.")
            # smth
            elif command.lower() == "stop" or command.lower() == "kill" or command.lower() == "exit" or command.lower() == "/stop" or command.lower() == "/kill" or command.lower() == "/exit":
                serverActive = False
                break
            # smth
            elif command.lower() == "ip" or command.lower() == "/ip":
                print("Something.")

            elif command.lower().__contains__("/all"):
                print("Announced to everyone.")
                print(command.replace("/all", ""))

            elif command.lower() == "clear" or command.lower() == "/clear":
                clearTerminal()

    print("Server Not active exited sendCommandThread")


def mainThread():
    global serverActive

    if serverActive:
        while True:
            if serverActive:
                read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

                for notified_socket in read_sockets:
                    if notified_socket == server_socket:
                        client_socket, client_address = server_socket.accept()

                        user = receive_message(client_socket)
                        if user is False:
                            continue

                        sockets_list.append(client_socket)

                        clients[client_socket] = user

                        # New connection.
                        print(
                            f"\nAccepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}",
                            end="")
                        print(f"\nServer > ", end="")

                    else:
                        message = receive_message(notified_socket)
                        if message is False:
                            print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                            print(f"\nServer > ", end="")
                            sockets_list.remove(notified_socket)
                            del clients[notified_socket]
                            continue

                        user = clients[notified_socket]

                        print(
                            f"\n(Received message from {user['data'].decode('utf-8')}): {message['data'].decode('utf-8')}",
                            end="")
                        print(f"\nServer > ", end="")

                        for client_socket in clients:
                            if client_socket != notified_socket:
                                client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

                for notified_socket in exception_sockets:
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]

            elif not serverActive:
                print("Server Not active exited mainThread")
                break
    else:
        print("Exiting...")
        sys.exit()


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


# Threads
mainThread = threading.Thread(target=mainThread, name="mainThread")
sendThread = threading.Thread(target=send_command, name="sendThread")


def main():
    sendThread.start()
    mainThread.start()
    sendThread.join()
    mainThread.join()

if __name__ == '__main__':
    serverActive = True
    main()
