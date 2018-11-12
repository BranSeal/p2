# README
Name: Brandon Seal
bseal3
CS 3251

I wasn't able to get multiplayer to work in time, but singleplayer should be working fine.
Singleplayer ran correctly on GT shuttle server while I was using my machine.

### Design
    As for my implementation ideas, I used python's _thread module to handle all the individual client connections.
    Using bytes and bytearrays I constructed my messages to send and receive between client and server.
    Client would perform very minimal error detection from input.  For example, it would check if an incorrect guess was guessed or not based on
    the most recent game message.
    
    When it came to writing multiplayer, I was having trouble ensuring that each client could interact with the server and
    have the server correctly delegate the correct tasks and messages to a client.
    I figured it would be best to have global variables keeping track of what rooms were occupied and what player number a thread had.
    But, as I got further along it became more and more complicated due to proper planning ahead of time.
    
### Distribution of work
    This project was done solo, so all work here is my own.
    
# To run the application
    
## To connect to a shuttle server, enter in shell:
    $ ssh [student-id]@cc-shuttle1.cc.gatech.edu
    where [student-id] is your own student ID. In my case, bseal3.

## In a separate shell, enter:
    scp server.py [student-id]@cc-shuttle1.cc.gatech.edu:/nethome/[student-id]

## Based on piazza post ID 175, do the following to install python 3.4.5 onto a shuttle server.

    1) SSH into shuttles and then download python3 into your home directory

    $ cd ~/
    $ wget https://www.python.org/ftp/python/3.4.5/Python-3.4.5.tgz

    2) Change the access permission of the execution file in Python to executable. 

    $ tar zxfv Python-3.4.5.tgz
    $ find ~/Python-3.4.5 -type d | xargs chmod 0755
    $ cd Python-3.4.5

    3) Configure the installation directory. 

    $ ./configure --prefix=$HOME/Python-3.4.5
    $ make
    $ make install

    4) Add the path of Python to the shell script that Bash runs whenever it is started interactively.

    $ vim ~/.bashrc

    Add the following  line to the file:

    export PATH=$HOME/Python-3.4.5/:$PATH

    5) Reload the shell script

    $ source ~/.bashrc

## After successfully compiling python and adding to path, execution of 'which python' should return 3.4.5

## Obtain the IP address of the shuttle server by typing
    $ ifconfig
    The address should be under eth0 as inet addr.

## To run the server, execute in the shuttle:
    $ python server.py [Port Number]

## Then using the IP obtained from the shuttle, run the client in a separate shell:
    $ python client.py [IP Address] [Port Number]
    The port number should be the same port as the server's.

