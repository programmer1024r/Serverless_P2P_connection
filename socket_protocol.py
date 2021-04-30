import file_management
import consts
import socket
# Message flow format:
#------------------------------------------------------------------------------
def sending(socket, data):
    """
    Use: send data in a live socket 
    Input: socket(socket Object), data(str), file_name(str)
    Output: None
    """
    send_msg = data.encode()

    msg_len = len(data)

    send_len = str(msg_len).encode()
    # Make the header in a perfect length
    send_len += b' ' * (consts.HEADER - len(send_len))

    socket.send(send_len)
    socket.send(send_msg)

def receiving(socket):
    """
    Use: receive data in a live socket
    Input: socket(socket Object)
    Output: data(str)
    """

    # Reveiving header
    msg_header = socket.recv(consts.HEADER).decode()

    if msg_header:
        # reading header:
        msg_len = int(msg_header)

        data = socket.recv(msg_len).decode()
    return data
#------------------------------------------------------------------------------



# Handlers
#------------------------------------------------------------------------------
def sending_handler(live_connection, file_path):
    """
    Use: send/recieve a file and close the connection
    Input: live_connection(socket Object), state(int)
    Output: None
    """

    file_data = file_management.take_file_data(file_path)
    file_name = file_management.find_name(file_path)
    sending(live_connection, file_name)
    sending(live_connection, file_data)
        
    live_connection.close()
#------------------------------------------------------------------------------
def receiving_handler(live_connection):
    """
    Use: receiving new file and open it on the computer
    Input: live_connection(socket Object)
    Output: None
    """
    file_name = receiving(live_connection)
    file_data = receiving(live_connection)
    # create a text file on desktop with file data
    file_management.create_file(file_data, file_name)

    live_connection.close()
#------------------------------------------------------------------------------