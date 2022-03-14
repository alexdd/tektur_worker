#    Tektur Worker - Camuda external task executor for ETL processes 
#    Copyright (C) 2020 - 2025  Alex Duesel, tekturcms@gmail.com

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
        ["delete"] -- flag wether the source folder should be deleted or not
    """

    folder_to_move = os.path.join(process_dir, variables["source-folder"]["value"])
    location = variables["location"]["value"]
    destination = os.path.join(process_dir, variables["destination-folder"]["value"])
    delete = variables["delete"]["value"]
    os.makedirs(destination, exist_ok=True)

    if location == "external":
        dest_folder = destination
    else:
        dest_folder = os.path.join(process_dir, destination)
        
    try:
        forced_folder_copy(folder_to_move, dest_folder)
    except Exception as e:
        raise TaskError("MOVE FOLDER Error!", str(e))
    
    if delete == "yes":
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

def delete_path(process_dir, variables):
    
    """This task removes the folder structure given by the provided path

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["path"] -- The relative path  to create the directories for e.g. psth/to/desst
    """
    
    path = os.path.join(process_dir, variables["path"]["value"])
    shutil.rmtree(path, ignore_errors=True)
    return {}

def write_data(process_dir, variables):
    
    """This task writes string data to a file

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["path"] -- The relative path write the data to
        ["data"] -- The string to be written to the filesystem
    """
    
    path = os.path.join(process_dir, variables["path"]["value"])
    data = str(variables["data"]["value"])
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    f = open(path, "w")
    f.write(data)
    f.close()
    return {}

def read_data(process_dir, variables):
    
    """This task reads string data from a file

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["path"] -- The relative path where the file to be read is located
        ["data"] -- The data string to be written to the filesystem
    """
    
    path = os.path.join(process_dir, variables["path"]["value"])
    return {"data": {"value": open(path,"r").read()}}
