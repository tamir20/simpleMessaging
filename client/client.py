import re
import time
import json
import socket
import threading

def heartbeat_message(connection: socket.socket, name: str, port: int) -> None:
    '''
        send heartbeat message to server
    '''
    heartbeat = {
        'name': name,
        'port': port
    }

    while True:
        try:
            connection.send(json.dumps(heartbeat).encode())

        except Exception:
            print(f'Error sending heartbeat message')
            connection.close()
            break

        time.sleep(5)

def handle_messages(connection: socket.socket):
    '''
        Receive messages sent by the server and display them to user
    '''

    while True:
        try:
            msg = connection.recv(1024)

            # If there is no message, there is a chance that connection has closed
            # so the connection will be closed and an error will be displayed.
            # If not, it will try to decode message in order to show to user.
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Error handling message from server: {e}')
            connection.close()
            break

def get_port_not_in_use() -> int:
    for port in range(12000,13001):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)):
                return port

def server(port: int) -> None:
    '''
        Main process that receive client's connections and start a new thread
        to handle their messages
    '''

    LISTENING_PORT = port
    
    try:
        # Create server and specifying that it can only handle 4 connections by time!
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Started accepting messages')
        
        while True:

            # Accept client connection
            socket_connection, address = socket_instance.accept()
            # Start a new thread to handle client connection and receive it's messages
            # in order to send to others connections
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        socket_instance.close()

def handle_user_connection(connection: socket.socket, address: str) -> None:
    '''
        Get user connection in order to keep receiving their messages and
        sent to others users/connections.
    '''
    while True:
        try:
            # Get client message
            msg = connection.recv(1024)

            # If no message is received, there is a chance that connection has ended
            # so in this case, we need to close connection and remove it from connections list.
            if msg:
                # Log message sent by user
                print(f'{msg.decode()}')

        except Exception as e:
            #print(f'Error to handle user connection: {e}')
            connection.close()
            break

def client() -> None:
    '''
        Main process that start client connection to the server 
        and handle it's input messages
    '''

    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 12000
    id = 0
    current_socket_instance = None

    try:
        # Instantiate socket and start connection with server
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        # Create a thread in order to handle messages sent by server
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        print('Enter Name:')
        name = input()
        port = get_port_not_in_use()
        # Create a thread to send heartbeat to server
        threading.Thread(target=heartbeat_message, args=[socket_instance, name, port]).start()
        threading.Thread(target=server, args=[port]).start()

        # Read user's input until it quit from chat and close connection
        while True:
            msg = input()

            if msg == 'quit':
                break
            if msg == 'list':
                socket_instance.send(msg.encode())
            else:
                if msg == 'help':
                    print('please state your destination id using "id <id>". to see available ids please use "list". see your name using "name"')
                else:
                    if msg == 'name':
                        print(name)
                    else:
                        pattern = re.compile(r"^id \d+$")
                        if pattern.match(msg):
                            id_number = int(msg.split()[1])
                            print(f"id is now set to: {id_number}")
                            id = id_number
                            if current_socket_instance is not None:
                                current_socket_instance.close()
                            current_socket_instance = socket.socket()
                            current_socket_instance.connect((SERVER_ADDRESS, id))
                        else:
                            if id == 0:
                                print('please state your destination id using "id <id>". to see available ids please use "list". see your name using "name"')
                            else:
                                current_socket_instance.send((f"From {name}: {msg}").encode())

        # Close connection with the server
        socket_instance.close()
        current_socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()


if __name__ == "__main__":
    client()
