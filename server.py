from socket import *
import _thread
import sys
import argparse
import random

num_games = 0
words = ['honey', 'feline', 'palace',
         'poetry', 'attempt', 'floating',
         'cookies', 'calm', 'canal',
         'August', 'Autumn', 'breeze',
         'contrast', 'cookies', 'damage']

rooms = ["empty", "empty", "empty"]
room_words = ['', '', '']
room_lock = _thread.allocate_lock()
turn_lock = _thread.allocate_lock()

def on_new_client(clientsocket, addr):
    global num_games
    global rooms
    global room_lock
    room = -1
    msg = clientsocket.recv(30)
    
    # Singleplayer
    if msg[0] == 0:
        if num_games < 3:
            room_lock.acquire()
            for i in range(len(rooms)):
                if rooms[i] == "empty":
                    rooms[i] = "full"
                    num_games += 1
                    room = i
                    print("- Game started in room {}".format(room))
                    room_lock.release()
                    break
        else:
            print('- Connection attempted while server is full')
            message = construct_text_msg('server-overloaded')
            clientsocket.send(message)
            clientsocket.close()
            return
        word = words[random.randint(0, len(words) - 1)]
        print("- {} chosen for {}".format(word, addr))
        current = empty_game_str(len(word))
        incorrect = ''

        msg = construct_game_msg(current, incorrect)

        clientsocket.send(msg)
        print('- Sent packet {} to {}'.format(msg, addr))

        while True:
            guess = clientsocket.recv(30)
            if guess != bytes() and guess[0] == 1:
                print("- Received a correct formatted guess: {}".format(chr(guess[1])))
                guess_letter = chr(guess[1])
                if guess_letter in word:
                    current = correct_guess(current, word, guess_letter)
                    if "_" not in current:
                        msg = construct_text_msg('You win!')
                        print(msg)
                        clientsocket.send(msg)
                        print('- Sent packet {} to {}'.format(msg, addr))
                        break
                else:
                    incorrect += guess_letter
                    if len(incorrect) == 6:
                        msg = construct_text_msg('You lose :(')
                        print(msg)
                        clientsocket.send(msg)
                        print('- Sent packet {} to {}'.format(msg, addr))
                        break
                msg = construct_game_msg(current, incorrect)
                print(msg)
                clientsocket.send(msg)
                print('- Sent packet {} to {}'.format(msg, addr))
    
    # Multiplayer
    elif msg[0] == 2:
        playerID = 0
        player_turn = 0
        if num_games < 3:
            room_lock.acquire()
            for i in range(len(rooms)):
                if rooms[i] == "waiting":
                    rooms[i] = "full"
                    room = i
                    playerID = 2
                    message = construct_text_msg('Waiting on Player 1...')
                    turn_lock.acquire()
                    print("- Game has started in room {}".format(room))
                if rooms[i] == "empty":
                    rooms[i] = "waiting"
                    num_games += 1
                    room = i
                    playerID = 1
                    print("- Player 1 waiting in room {}".format(room))
                    turn_lock.acquire()
                    room_lock.release()
                    break
            room_lock.release()
            print('- Connection attempted while server is full')
            message = construct_text_msg('server-overloaded')
            clientsocket.send(message)
            clientsocket.close()
        else:
            print('- Connection attempted while server is full')
            message = construct_text_msg('server-overloaded')
            clientsocket.send(message)
            clientsocket.close()
            return

        while True:
            guess = clientsocket.recv(30)
            if guess != bytes() and guess[0] == 1:
                print("- Received a correct formatted guess: {}".format(chr(guess[1])))
                guess_letter = chr(guess[1])
                if guess_letter in word:
                    current = correct_guess(current, word, guess_letter)
                    if "_" not in current:
                        msg = construct_text_msg('You win!')
                        print(msg)
                        clientsocket.send(msg)
                        print('- Sent packet {} to {}'.format(msg, addr))
                        break
                else:
                    incorrect += guess_letter
                    if len(incorrect) == 6:
                        msg = construct_text_msg('You lose :(')
                        print(msg)
                        clientsocket.send(msg)
                        print('- Sent packet {} to {}'.format(msg, addr))
                        break
                msg = construct_game_msg(current, incorrect)
                print(msg)
                clientsocket.send(msg)
                print('- Sent packet {} to {}'.format(msg, addr))


        

        for i in range(len(rooms)):
            if rooms[i] == "waiting":
                rooms[i] = "full"
                player = 2
                room = i
                break
            if rooms[i] == "empty":
                room[i] = "waiting"
                player = 1
                break
        return


    clientsocket.close()
    room_lock.acquire()
    rooms[room] = "empty"
    num_games -= 1
    room_lock.release()

def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    host = gethostname()
    print('Host name: {}'.format(host))
    p = argparse.ArgumentParser()
    p.add_argument("port", type=int)
    args = p.parse_args()
    port = args.port 
    
    print('Server started!')
    print('Waiting for clients...')

    s.bind((host, port))
    s.listen(0)

    while True:
        c, addr = s.accept()
        print("Connection started with {}".format(addr))
        _thread.start_new_thread(on_new_client, (c, addr))
        # c, addr = s.accept()
        # print('- Connection attempted while is full')
        # message = construct_text_msg('server-overloaded')
        # c.send(message)
        # c.close()
    s.close()

def construct_game_msg(current, incorrect):
    constructed_m = bytearray(b'\x00')
    constructed_m.append(len(current))
    constructed_m.append(len(incorrect))
    for c in current:
        constructed_m.append(ord(c))
    for c in incorrect:
        constructed_m.append(ord(c))
    return bytes(constructed_m)

def construct_text_msg(m):
    constructed_m = bytearray(b'\xFF')
    for c in m:
        constructed_m.append(ord(c))
    return bytes(constructed_m)

def empty_game_str(word_length):
    new_word = ''
    for i in range(word_length):   
        new_word += '_'
    return new_word

def correct_guess(current, word, guess_letter):
    current_list = list(current)
    for i in range(len(current)):
        if (word[i] == guess_letter):
            current_list[i] = guess_letter
    return ''.join(current_list)

if __name__ == "__main__":
    main()


