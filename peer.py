# Modules
import socket, threading 
# Porject Files
import socket_protocol, consts

# Peer algorithm
class Peer():

    def __init__(self, ip, port):
        self.ip = ip 
        self.port = port 
        self.address = (self.ip, self.port)
        # Run the peer
        self.run()

    def client_conn_to_peer(self): # with the GUI
        """
        Use: create a live socket by connecting from the GUI to the desired peer 
        Input: None
        Output: None
        """
        while True:
            # Create the TCP/IP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # the sockets closes in their handlers
            # GUI function
            addr = input("Enter the desired peer (server) IP \n"), self.port

            print("Enter your choosen file path")
            file_path = input(r"")
            # conncting to the peer server (three-way hand shake) live connection
            try:
                client_socket.connect(addr)
            
                print("You have been succesfuly connected!")
                # create a new thread, args = live connection , the handler state
                client_thread = threading.Thread(target=socket_protocol.sending_handler, args=(client_socket, file_path)) 
                client_thread.start()
        
            except Exception as e:
                print(f"Error:\n{e}\n")
                try: 
                    client_socket.close()
                except:
                    pass

    #------------------------------------------------------------------------------
    def peer_accept_client(self):
        """
        Use: create a live socket by listening for requests from other peers
        Input: None
        Output: None
        """

        # Create the TCP/IP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # the socket is server type, to this machine
            server_socket.bind(self.address)
            # Listening can accept 10 incoming sockets at the same time
            server_socket.listen(10)

            while True:
                # accept a new connection
                client, addr = server_socket.accept()
                print(f"[New Connection] {addr} connected")
                # add thread for the new connection
                server_thread = threading.Thread(target=socket_protocol.receiving_handler, args=(client,))
                server_thread.start()

        except Exception as e:
            print(f"Error:{e}")
            try: 
                client_socket.close()
            except:
                pass
    #------------------------------------------------------------------------------

    def run(self):
        """
        Use: start runing the two main threads of the peer 
                "server and client"
        Input: None
        Output: None
        """

        #--------------Connetction Makers--------------
        # Client
        father_client_thread = threading.Thread(target=self.client_conn_to_peer) 
        father_client_thread.start()
        # Server
        father_server_thread = threading.Thread(target=self.peer_accept_client) 
        father_server_thread.start()
        # the threads close by themselfs after returnig from their target function


# Make this file act like a library
if __name__ == "__main__":

    Peer(consts.IP, consts.PORT)

