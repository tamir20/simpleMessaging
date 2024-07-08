import socket
import threading
import json
import time

# Global variable that mantain client's connections
online_users = {}

def handle_user_connection(connection: socket.socket, address: str) -> None:
    '''
        Get user connection in order to keep receiving their messages and
        sent to others users/connections.
    '''
    while True:
        time.sleep(1)
        try:
            # Get client message
            msg = connection.recv(1024)

            # If no message is received, there is a chance that connection has ended
            # so in this case, we need to close connection and remove it from connections list.
            if msg:
                # Log message sent by user
                print(f'{address[0]}:{address[1]} - {msg.decode()}')
                
                # Build message format and broadcast to users connected on server
                #msg_to_send = f'From {address[0]}:{address[1]} - {msg.decode()}'
                #broadcast(msg_to_send, connection)

                if msg.decode() == "list":
                    title = f"{'Name':10} {'ID'}"
                    connection.send(title.encode())
                    divider = f"----------------\n"
                    connection.send(divider.encode())
                    for d in online_users.values():
                        user = f"{d['name']:10} {d['port']}\n"
                        connection.send(user.encode())
                    #connection.send(str(online_users.values()).encode())
                else:
                    try:
                        heartbeat = json.loads(msg.decode())
                        if connection not in online_users.keys():
                            online_users[connection] = heartbeat
                    except Exception as e:
                        print(f'failed to parse json string: {e}')

        except Exception as e:
            print(f'A connection was closed')
            remove_connection(connection)
            break

def remove_connection(conn: socket.socket) -> None:
    '''
        Remove specified connection from connections list
    '''

    if conn in online_users:
        del online_users[conn]


def server() -> None:
    '''
        Main process that receive client's connections and start a new thread
        to handle their messages
    '''

    LISTENING_PORT = 12000
    
    try:
        # Create server and specifying that it can only handle 4 connections by time!
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Server running!')
        
        while True:

            # Accept client connection
            socket_connection, address = socket_instance.accept()
            # Start a new thread to handle client connection and receive it's messages
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        socket_instance.close()


if __name__ == "__main__":
    server()