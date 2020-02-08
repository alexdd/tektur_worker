import os
from subprocess import Popen, PIPE
from settings import EXIST_DB_CLIENT
from errors import TaskError


def exist_load(process_dir, variables):
    
    """This task stores XML files in an exist-db via CLI.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictonary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["inputFolder"] -- The name of the folder containing the input files
        ["dbPath"] -- The path on the exist-db where the files will be stored
    """
    
    input_folder = os.path.join(process_dir, variables["inputFolder"]["value"])
    db_path = variables["dbPath"]["value"]
    args = [
        EXIST_DB_CLIENT,
        "-c",
        db_path,
        "-p",
        input_folder
        ]    
    print(" ".join(args))
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == -1:
        raise TaskError("exist-db load error!", "Input folder: "+input_folder+" XSLT: "+db_path)
    elif len(err) > 0:
        raise TaskError("exist-db load error!", err.decode())
    return {}

