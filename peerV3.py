import socket, threading, sys, os
# Consts
HEADER = 64
FORMAT = 'utf-8'
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Peer algorithm
def client_conn_to_peer(): # with the GUI
    """
    Use: create a live socket by connecting from the GUI to the desired peer 
    Input: None
    Output: None
    """
    try:
        while True:
            # Create the TCP/IP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # GUI function
            addr = input("Enter the desired peer (server) IP \n"), port
            file_path = input(r"Enter your choosen file path")
            # conncting to the peer server (three-way hand shake) live connection
            client_socket.connect(addr)
            print("You have been succesfuly connected!")
            # create a new thread, args = live connection , the handler state
            client_thread = threading.Thread(target=handler, args=(client_socket, 2, file_path)) 
            client_thread.start()

    except KeyboardInterrupt:
        # ctrl + shift + c exit
        pass


def peer_accept_client():
    """
    Use: create a live socket by listening for requests from other peers
    Input: None
    Output: None
    """

    # Create the TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # the socket is server type, to this machine
    server_socket.bind(host)
    # Listening can accept 10 incoming sockets at the same time
    server_socket.listen(10)
    try:
        while True:
            # accept a new connection
            client, addr = server_socket.accept()
            print(f"[New Connection] {addr} connected")
            # add thread for the new connection
            server_thread = threading.Thread(target=handler, args=(client, 1))
            server_thread.start()

    except KeyboardInterrupt:
        # ctrl + shift + c exit
        pass

#------------------------------------------------------------------------------
def handler(live_connection, state, file_path=''):
    """
    Use: send/recieve a file and close the connection
    Input: live_connection(socket Object), state(int)
    Output: None
    """
    if state == 1:
        file_name = receiving(live_connection)
        file_data = receiving(live_connection)
        # create a text file on desktop with file data
        create_file(file_data, file_name)

    if state == 2:
        file_data = take_file_data(file_path)
        file_name = find_name(file_path)
        sending(live_connection, file_name)
        sending(live_connection, file_data)
        
    live_connection.close()
#------------------------------------------------------------------------------

    
#------------------------------------------------------------------------------
def take_file_data(file_path): 
    """
    Use: take file data 
    Input: file path(str)
    Output: file_data(str)
    """
    with open(file_path, 'r') as f:
        file_data = f.read()

    return file_data

def create_file(data, name):
    """
    Use: create a file on the desktop
    Input: data(str), name(str)
    Output: None
    """
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # won't work with linux:
    file_path = desktop + "\\" + name
    with open(file_path, 'w') as f:
        f.write(data)

#------------------------------------------------------------------------------
def find_name(file_path):
    """
    Use: extract a file name form his path 
    Input: file_path(str)
    Output: file_name(str)
    """
    folders_list = file_path.split('\\')
    return folders_list[-1]



#------------------------------------------------------------------------------
# weird bug!
def sending(socket, data):
    """
    Use: send data in a live socket 
    Input: socket(socket Object), data(str), file_name(str)
    Output: None
    """
    send_msg = data.encode(FORMAT)

    msg_len = len(data)

    send_len = str(msg_len).encode(FORMAT)
    # Make the header in a perfect length
    send_len += b' ' * (HEADER - len(send_len))

    socket.send(send_len)
    socket.send(send_msg)

def receiving(socket):
    """
    Use: receive data in a live socket
    Input: socket(socket Object)
    Output: data(str)
    """

    # Reveiving header
    msg_header = socket.recv(HEADER).decode(FORMAT)

    if msg_header:
        
        # reading header:
        msg_len = int(msg_header)

        data = socket.recv(msg_len).decode(FORMAT)
    return data
    
#------------------------------------------------------------------------------

def main():

    #--------------Connetction Makers--------------
    # Client
    father_client_thread = threading.Thread(target=client_conn_to_peer) 
    father_client_thread.start()
    # Server
    father_server_thread = threading.Thread(target=peer_accept_client) 
    father_server_thread.start()
    # the threads close by themselfs after returnig from their target function

#------------------------------------------------------------------------------


# Make this file act like a library
if __name__ == "__main__":

    # Variables:
    port = 9999
    ip = socket.gethostbyname(socket.gethostname())
    host = (ip, port)

    main()
