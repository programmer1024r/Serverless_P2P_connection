import os

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
    # make the user an option to choose were his files will auto save
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # won't work with linux:
    file_path = desktop + "\\" + name
    with open(file_path, 'w') as f:
        f.write(data)

def find_name(file_path):
    """
    Use: extract a file name form his path 
    Input: file_path(str)
    Output: file_name(str)
    """
    folders_list = file_path.split('\\')
    return folders_list[-1]