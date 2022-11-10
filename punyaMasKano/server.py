import socket, threading, random, os

# Global variable that mantain client's connections
connections = []
addresses = []
numbers = []
isTurns = []
nicknames = []

playerIndex = 0


def handle_user_connection(connection: socket.socket, address: str, index) -> None:
    """
    Get user connection in order to keep receiving their messages and
    sent to others users/connections.
    """
    while True:
        global isTurns
        global nicknames
        try:
            if isTurns[index] == True:
                # Get client message
                msg = connection.recv(1024)

                # If no message is received, there is a chance that connection has ended
                # so in this case, we need to close connection and remove it from connections list.
                if msg:
                    # Build message format and broadcast to users connected on server
                    if msg.decode() == "GAS":
                        rand = random.randint(1, 6)
                        numbers[index] += rand

                        # Log message sent by user
                        if index + 1 == len(isTurns):
                            os.system("CLS")
                            print(
                                f"{nicknames[index - 1]} - TOTAL : {numbers[index - 1]}\n{nicknames[index]} - TOTAL : {numbers[index]}"
                            )
                        else:
                            os.system("CLS")
                            print(
                                f"{nicknames[index]} - TOTAL : {numbers[index]}\n{nicknames[index + 1]} - TOTAL : {numbers[index + 1]}"
                            )

                        msg_to_send = f"{nicknames[index]} Roll - {str(rand)} - TOTAL : {numbers[index]}\n"
                        broadcast(msg_to_send, connection)

                        if numbers[index] >= 20:
                            broadcast(f"{nicknames[index]} WIN", connection)
                            for conn in connections:
                                remove_connection(conn)
                            break

                # Close connection if no message was sent
                else:
                    remove_connection(connection)
                    break

                if index + 1 == len(isTurns):
                    isTurns[index - 1] = True
                else:
                    isTurns[index + 1] = True
                isTurns[index] = False

        except Exception as e:
            print(f"Error to handle user connection: {e}")
            remove_connection(connection)
            break


def broadcast(message: str, connection: socket.socket) -> None:
    """
    Broadcast message to all users connected to the server
    """

    # Iterate on connections in order to send message to all client's connected
    for client_conn in connections:
        # Check if isn't the connection of who's send
        if client_conn != connection:
            try:
                # Sending message to client connection
                client_conn.send(message.encode())

            # if it fails, there is a chance of socket has died
            except Exception as e:
                print("Error broadcasting message: {e}")
                remove_connection(client_conn)


def remove_connection(conn: socket.socket) -> None:
    """
    Remove specified connection from connections list
    """

    # Check if connection exists on connections list
    if conn in connections:
        # Close socket connection and remove connection from connections list
        conn.close()
        connections.remove(conn)


def server() -> None:
    global connections
    global addresses
    global numbers
    global isTurns
    global playerIndex
    global nicknames
    """
    Main process that receive client's connections and start a new thread
    to handle their messages
    """

    LISTENING_PORT = 12000

    try:
        # Create server and specifying that it can only handle 4 connections by time!
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(("", LISTENING_PORT))
        socket_instance.listen(2)

        print("Server running!")

        while True:
            # Accept client connection
            socket_connection, address = socket_instance.accept()
            # Add client connection to connections list
            connections.append(socket_connection)
            addresses.append(address)
            numbers.append(0)
            nicknames.append("Player " + str(playerIndex + 1))

            if playerIndex == 0:
                isTurns.append(True)
            else:
                isTurns.append(False)

            # Start a new thread to handle client connection and receive it's messages
            # in order to send to others connections
            threading.Thread(
                target=handle_user_connection,
                args=[socket_connection, address, playerIndex],
            ).start()
            playerIndex += 1

    except Exception as e:
        print(f"An error has occurred when instancing socket: {e}")
    finally:
        # In case of any problem we clean all connections and close the server connection
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()


if __name__ == "__main__":
    server()
