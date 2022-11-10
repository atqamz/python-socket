import threading, socket, os

isPlay = False
player_id = 0
player_turn = 0
total = 0
number_answer = -1

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 59000))

print("You're Connected! Please Wait ...")

# recv message from server
def client_receive():
    global isPlay, player_id, player_turn, total, number_answer

    while True:
        try:
            # listening message from server
            message = client.recv(1024).decode("utf-8")

            # check if id? include in server's message
            if "id?" in message:
                isPlay = True
                temp = message.split(" ")
                player_id = int(temp[1])
                total = int(temp[2])

            elif "turn?" in message:
                temp = message.split(" ")
                player_turn = int(temp[1])

                os.system("CLS")
                print("BALAP KEONG!")
                print(f"You're Player-{player_id}")
                print(f"Total\t: {total}\n")

                if player_turn == player_id:
                    number_answer = int(input("Type 1 to play!\n"))
                else:
                    print(f"Please Wait ... Player-{player_turn}'s Turn")

            elif "gameover?" in message:
                temp = message.split(" ")
                winner = int(temp[1])
                total = int(temp[2])

                os.system("CLS")
                print("BALAP KEONG!")
                print(f"The Winner is Player-{winner}")
                print(f"Your Total\t: {total}\n")

            else:
                print(message)

        except:
            print("Error!")
            client.close()
            break


# sending message to server
def client_send():
    global isPlay, player_id, player_turn, number_answer

    while True:
        if isPlay == True and number_answer != -1:

            if number_answer == 1:
                message = f"{player_id} {number_answer}"
                client.send(message.encode("utf-8"))
                number_answer = -1
            else:
                number_answer = -1
                number_answer = int(input("Invalid Input! Type 1 to play!\n"))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
