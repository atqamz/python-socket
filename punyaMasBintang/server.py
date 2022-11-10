import threading, socket, os, random

player_total = 0
player_turn = 1
number_quest = 0

host = "127.0.0.1"  # ip for localhost
port = 59000  # port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # make server
server.bind((host, port))  # bind server to ip
server.listen(2)  # server listening

# store client and multiple choice
clients = []
choices = []

# broadcast from one to all client
def broadcast(message):
    for client in clients:
        client.send(message)


# handle client if messaging or leaving
def handle_client(client):
    global player_total, player_turn, number_quest, choices

    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            temp = message.split(" ")

            if int(temp[1]) != 0:
                player_turn = int(temp[0])
                number_quest -= choices[int(temp[1]) - 1]

            if player_turn == 1:
                player_turn = 2
            elif player_turn == 2:
                player_turn = 1

            if number_quest != 0:
                game()
            else:
                winner = player_turn
                if winner == 1:
                    winner = 2
                elif winner == 2:
                    winner = 1
                print("GAME OVER! The Winner is Player-{}".format(winner))

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
    global player_total, number_quest
    print("Server is running and listening ...")

    # server will always listening until player_total = 2
    while player_total < 2:
        client, address = server.accept()

        # count player total
        player_total += 1
        print(f"Player-{player_total} has joined the game room!")

        # storing to array
        clients.append(client)

        # open thread for handle client connection
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

    number_quest = random.randint(100, 150)
    game()


def game():
    global player_total, player_turn, number_quest, choices
    # send the playerId to connected client
    os.system("CLS")
    for index, client in enumerate(clients):
        client.send(f"id? {str(index + 1)}".encode("utf-8"))

    # random question and answer
    choices = random.sample(range(1, 11), 3)
    choiceTemp = ""

    print("Game Started!")
    print(f"The Number Quest is {number_quest}")
    print(f"Multiple Choice")
    for index, number in enumerate(choices):
        choiceTemp += f"{number} "
        print(f"{index + 1}. {number}")

    broadcast(f"turn? {number_quest} {player_turn} {choiceTemp}".encode("utf-8"))


if __name__ == "__main__":
    receive()
