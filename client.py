from socket import *
import sys
import argparse

player = 1

def main(host, port):
    
    if not is_ready():
            print("Quitting...") 
            return
    
    if not is_multiplayer():
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        s.send(bytes(b'\x00'))
        while True:
            message = s.recv(1024)
            if (len(message) != 0):
                if message[0] == 255:  
                    text = message[1:].decode()
                    if text == 'server-overloaded':
                        print('Server is full! Qutting...')
                        return
                    elif text == 'You win!':
                        print('You win!')
                    elif text == 'You lose :(':
                        print('You lose :(')
                        print('Game Over!')
                    return
                elif message[0] == 0:
                    word_length = message[1] 
                    num_incorrect = message[2]
                    current_word = message[3:3+word_length]
                    incorrect = bytearray()
                    if num_incorrect != 0:
                        incorrect = message[3+word_length:]
                    print_message(current_word.decode(), incorrect.decode())
                    guess = ''
                    while True:
                        guess = input("Letter to guess: ")
                        if guess.lower() in incorrect.decode():
                            print("Error! Letter {} has been guessed before, please guess another letter.".format(guess))
                        elif len(guess) == 1 and guess.isalpha():
                            break
                        else:
                            print("Erorr! Please guess one letter.")
                    guess_message = bytearray()
                    guess_message.append(1)
                    guess_message.append(ord(guess.lower()))
                    guess_message = bytes(guess_message)
                    print(guess_message)
                    s.send(guess_message)

    else:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        s.send(bytes(b'\x02'))
        while True:
            message = s.recv(1024)
            if (len(message) != 0):
                if message[0] == 255:  
                    text = message[1:].decode()
                    if text == 'server-overloaded':
                        print('Server is full! Qutting...')
                        return
                    elif text == 'You win!':
                        print('You win!')
                    elif text == 'You lose :(':
                        print('You lose :(')
                        print('Game Over!')
                    elif text == 'Waiting on Player 1...':
                        print('Waiting on Player 1...')
                    elif text == 'Waiting on Player 2...':
                        print('Waiting on Player 2...')
                elif message[0] == 0:
                    word_length = message[1] 
                    num_incorrect = message[2]
                    current_word = message[3:3+word_length]
                    incorrect = bytearray()
                    if num_incorrect != 0:
                        incorrect = message[3+word_length:]
                    print("Your Turn!")
                    print_message(current_word.decode(), incorrect.decode())
                    guess = ''
                    while True:
                        guess = input("Letter to guess: ")
                        if guess.lower() in incorrect.decode():
                            print("Error! Letter {} has been guessed before, please guess another letter.".format(guess))
                        elif len(guess) == 1 and guess.isalpha():
                            break
                        else:
                            print("Erorr! Please guess one letter.")
                    guess_message = bytearray()
                    guess_message.append(1)
                    guess_message.append(ord(guess.lower()))
                    guess_message = bytes(guess_message)
                    print(guess_message)
                    s.send(guess_message)



def print_message(current_word, incorrect):
    print_current = ''
    for c in current_word:
        print_current += c
        print_current += ' '
    print(print_current)
    print_incorrect = ''
    for c in incorrect:
        print_incorrect += c
        print_incorrect += ' '
    print('Incorrect Guesses: {}\n'.format(print_incorrect))


def is_ready():
    start = input("Ready to start game? (y/n):")
    while True:
        if start == "y":
            return True
        elif start == "n":
            return False
        else:
            start = input("Invalid input! Try again: ")

def is_multiplayer():
    user_reply = input("Two player? (y/n): ")
    while True:
        if user_reply == "y":
            return True
        elif user_reply == "n":
            return False
        else:
            user_reply = input("Invalid input! Try again: ")

if __name__== "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("host")
    p.add_argument("port", type=int)
    args = p.parse_args()
    host = args.host
    port = args.port
    main(host, port)
