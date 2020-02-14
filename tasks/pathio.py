import os, shutil
from errors import TaskError

def forced_folder_copy(root_src_dir, root_dst_dir):

    '''walk subdirectory and force copy files and folders'''
    
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def move_folder(process_dir, variables):
    
    """This task moves a folder to a new destination inside the process
       working dir or to an external destination.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["folder-to-move"] -- The name of the folder that is going to be moved
        ["location"] -- switch between "process-dir" or "external" (absolute path)
        ["destination"] -- destination folder
    """

    folder_to_move = os.path.join(process_dir, variables["source-folder"]["value"])
    location = variables["location"]["value"]
    destination = os.path.join(process_dir, variables["destination-folder"]["value"])
    os.makedirs(destination, exist_ok=True)

    if location == "external":
        dest_folder = destination
    else:
        dest_folder = os.path.join(process_dir, destination)
        
    try:
        forced_folder_copy(folder_to_move, dest_folder)
    except Exception as e:
        raise TaskError("MOVE FOLDER Error!", str(e))
    
    shutil.rmtree(folder_to_move, ignore_errors=True)
    return {}

def make_path(process_dir, variables):
    
    """This task creates the folder structure given by the provided path

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["path"] -- The relative path  to create the directories for e.g. psth/to/desst
    """
    
    path = os.path.join(process_dir, variables["path"]["value"])
    os.makedirs(path, exist_ok=True)
    return {}

    
    
  
 