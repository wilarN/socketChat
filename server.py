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

globalLogPath = "./logs/globalLogFile.txt"
usrLogPath = "./logs/usrLogs/"

def createUserLogfile(usr_name):
    if not os.path.exists(f"./logs/usrLogs/{usr_name}.txt"):
        usrFile = open(f"./logs/usrLogs/{usr_name}.txt", "x")
        usrFile.close()
        usrFile = open(f"./logs/usrLogs/{usr_name}.txt", "w")
        usrFile.write(f"[-[ {usr_name} LOGFILE ]-]\n--------------------\n")
        usrFile.close()


def createGlobalLogFile():
    if not os.path.exists("./logs/globalLogFile.txt"):
        logFile = open("./logs/globalLogFile.txt", "x")
        logFile.close()


def read_from_logfile(path_to_file):
    if os.path.exists(path_to_file):
        read_file = open(path_to_file, "r")
        data = read_file.read()
        print(data)
        return data

def write_to_file(text_to_write, path_to_file):
    if os.path.exists(path_to_file):
        write_file = open(path_to_file, "w")
        write_file.write(text_to_write)


def logOutput(msg, logType):
    # Log
    if logType == 1:
        # print("\n[ LOG ] " + msg)
        write_to_file("\n[ LOG ]" + msg, globalLogPath)
    # Error
    elif logType == 2:
        # print("\n[ ERROR ] " + msg)
        write_to_file("\n[ ERROR ]" + msg, globalLogPath)
    # Warning
    elif logType == 3:
        # print("\n[ WARNING ] " + msg)
        write_to_file("\n[ WARNING ]" + msg, globalLogPath)


def clearTerminal():
    clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    clearConsole()


def send_command():
    global serverActive
    while serverActive:
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

    while serverActive == True:
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
                createUserLogfile(user['data'].decode('utf-8'))
                logOutput("Created User logfile.", 1)

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

    print("[2]Server Not active exited mainThread")


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
    if not os.path.exists('./logs'):
        os.makedirs('./logs')
    if not os.path.exists('./logs/usrLogs'):
        os.makedirs('./logs/usrLogs')
    createGlobalLogFile()
    # createUserLogfile("test")

    sendThread.start()
    mainThread.start()
    # sendThread.join()
    # mainThread.join()


if __name__ == '__main__':
    serverActive = True
    main()