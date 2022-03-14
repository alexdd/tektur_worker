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

import os
from subprocess import Popen, PIPE
from settings import EXIST_DB_CLIENT, EXIST_DB_SERVER_PORT
from errors import TaskError


def exist_load(process_dir, variables):
    
    """This task stores XML files in an exist-db via CLI.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["inputFolder"] -- The name of the folder containing the input files in the process dir
        ["dbPath"] -- The path on the exist-db where the files will be stored
    """
    
    input_folder = os.path.join(process_dir, variables["inputFolder"]["value"])
    db_path = variables["dbPath"]["value"]
    args = [
        EXIST_DB_CLIENT,
        "-ouri=xmldb:exist://"+EXIST_DB_SERVER_PORT+"/exist/xmlrpc/"
        "-c",
        db_path,
        "-p",
        input_folder
        ]    
    print(args)
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == -1:
        raise TaskError("exist-db load error!", "Input folder: "+input_folder+" DB Path: "+db_path)
    elif len(err) > 0:
        raise TaskError("exist-db load error!", err.decode())
    return {}

