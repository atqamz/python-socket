import threading, socket, os

isPlay = False
player_id = 0
player_turn = 0
number_answer = -1
number_quest = 0
answer = [0, 0, 0]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 59000))

print("You're Connected! Please Wait ...")

# recv message from server
def client_receive():
    global isPlay, player_id, player_turn, number_quest, number_answer, answer

    while True:
        try:
            # listening message from server
            message = client.recv(1024).decode("utf-8")

            # check if id? include in server's message
            if "id?" in message:
                isPlay = True
                temp = message.split(" ")
                player_id = int(temp[1])

            elif "turn?" in message:
                temp = message.split(" ")
                number_quest = int(temp[1])
                player_turn = int(temp[2])

                os.system("CLS")
                print("MINUS MATH START!")
                print(f"You're Player-{player_id}\n")
                print(f"NUMBER QUEST IS {number_quest}")

                if player_turn == player_id:
                    for index, number in enumerate(answer):
                        answer[index] = int(temp[index + 3])
                        print(f"{index + 1}. {answer[index]}")

                    print("0. Shuffle Multiple Choice")
                    number_answer = int(input("Choose 1/2/3: "))
                else:
                    print(f"Please Wait ... Player-{player_turn}'s Turn")

            else:
                print(message)

        except:
            print("Error!")
            client.close()
            break


# sending message to server
def client_send():
    global isPlay, player_id, player_turn, number_quest, number_answer, answer

    while True:
        if isPlay == True and number_answer != -1:
            print(answer[number_answer - 1])
            print(number_quest)

            if number_answer == 0:
                message = f"{player_id} {number_answer}"
                client.send(message.encode("utf-8"))
                number_answer = -1
            elif (
                number_answer >= 1
                and number_answer <= 3
                and answer[number_answer - 1] <= number_quest
            ):
                message = f"{player_id} {number_answer}"
                client.send(message.encode("utf-8"))
                number_answer = -1
            else:
                number_answer = -1
                number_answer = int(input("Invalid Choice ... Choose 1/2/3: "))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
