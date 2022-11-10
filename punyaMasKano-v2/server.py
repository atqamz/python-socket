import threading, socket, os, random

player_total = 0
player_turn = 1

isWin = False
winner = 0
rand = 0

host = "127.0.0.1"  # ip for localhost
port = 59000  # port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # make server
server.bind((host, port))  # bind server to ip
server.listen()  # server listening

# store client and multiple choice
clients = []
numbers = []

# broadcast from one to all client
def broadcast(message):
    for client in clients:
        client.send(message)


# handle client if messaging or leaving
def handle_client(client):
    global player_total, player_turn, winner, isWin, numbers, rand

    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            temp = message.split(" ")

            if int(temp[1]) == 1:
                print()
                player_turn = int(temp[0])

                rand = random.randint(1, 6)
                numbers[player_turn - 1] += rand

            if numbers[player_turn - 1] >= 20:
                winner = player_turn
                isWin = True

            if player_turn == 1:
                player_turn = 2
            elif player_turn == 2:
                player_turn = 1

            if isWin == False:
                rand = 0
                game()
            else:
                os.system("CLS")

                print("\nPlayer-1 total\t: {}".format(numbers[0]))
                print("Player-2 total\t: {}".format(numbers[1]))
                print("GAME OVER! The Winner is Player-{}".format(winner))

                for index, client in enumerate(clients):
                    client.send(
                        f"gameover? {str(winner)} {numbers[index]}".encode("utf-8")
                    )

        except:
            # remove and closing connection
            index = clients.index(client)
            clients.remove(client)
            client.close()

            print(f"Player-{index + 1} has left the game room!")
            player_total -= 1
            break


# server when receiving
def receive():
    global player_total, clients, numbers
    print("Server is running and listening ...")

    # server will always listening until player_total = 2
    while player_total < 2:
        client, address = server.accept()

        # count player total
        player_total += 1
        print(f"Player-{player_total} has joined the game room!")

        # storing to array
        clients.append(client)
        numbers.append(0)
        print(numbers)

        # open thread for handle client connection
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

    game()


def game():
    global player_total, player_turn, numbers

    # send the playerId to connected client
    os.system("CLS")
    for index, client in enumerate(clients):
        client.send(f"id? {str(index + 1)} {numbers[index]}".encode("utf-8"))

    print("BALAP KEONG Started!")
    print("Player-{} turn\n".format(player_turn))
    print("Player-1 total\t: {}".format(numbers[0]))
    print("Player-2 total\t: {}".format(numbers[1]))

    broadcast(f"turn? {player_turn}".encode("utf-8"))


if __name__ == "__main__":
    receive()
