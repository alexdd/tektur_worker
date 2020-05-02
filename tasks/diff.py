#    Tektur Worker - Camuda external task executor for ETL processes 
#    Copyright (C) 2020  Alex Duesel, tekturcms@gmail.com

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
from subprocess import call, Popen, PIPE
from tempfile import NamedTemporaryFile
from errors import TaskError
from settings import *

def differ(input_file1, input_file2):
    
    '''executes GNU diff brief command on two normalized XML files and returns
       True if the files differ'''

    result = False
    if not os.path.exists(input_file2):
        result = True
    else:
        diff_file1 = NamedTemporaryFile(delete=False)
        diff_file2 = NamedTemporaryFile(delete=False)
        args = [
            XMLLINT_CMD,
            "--c14n",
            input_file1]
        try:
            call(args,stdout=diff_file1)
        except:
            raise TaskError("DIFF Error!", "Source: "+input_file1)
        args = [
            XMLLINT_CMD,
            "--c14n",
            input_file2]
        try:
            call(args,stdout=diff_file2)
        except:
            result = True
        if not result:
            args = [
                DIFF_CMD,
                "-q",
                diff_file1.name,
                diff_file2.name]
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()
            if p.returncode == -1:
                raise TaskError("DIFF Error!", "Source: "+input_file1)
            elif len(err) > 0:
                raise TaskError("DIFF Error!", err.decode())
            elif len(output) > 0:
                result = True
        diff_file1.close()
        diff_file2.close()
        os.unlink(diff_file1.name)
        os.unlink(diff_file2.name) 
    return result
    
def batch_compare_xml(process_dir, variables):
    
    """This task compares an xml file in the one folder with the corresponding 
       xml file in the other folder and return a list of filenames of the 
       files that differ - only looking at the files in the source-folder.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["source-folder"] -- The name of the folder that is going to be compared
        ["folder-to-compare-to"] -- The name of the other folder
        ["delta"] -- Output variable containing the list of 
                     filenames of the xml files that differ
    """

    source_folder = os.path.join(process_dir, variables["source-folder"]["value"])
    folder_to_compare_to = os.path.join(process_dir, variables["folder-to-compare-to"]["value"])
    delta = []
    for file_name in os.listdir(source_folder): 
        if os.path.isdir(file_name) or not file_name.endswith('.xml'):
            continue
        input_file1 =  os.path.join(process_dir, source_folder, file_name)    
        input_file2 =  os.path.join(process_dir, folder_to_compare_to, file_name) 
        if differ(input_file1, input_file2):
            delta.append(file_name)
    return {"delta": {"value": delta }}

def compare_xml(process_dir, variables):
    
    """This task compares two xml files and returns a boolean flag if the files differ

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["source-file"] -- The name of the xml file that is going to be compared
        ["file-to-compare-to"] -- The name of the other file
        ["differ] -- Output bool variable containing the result of the diffing process
    """
    
    input_file1 =  os.path.join(process_dir, variables["source-file"]["value"])    
    input_file2 =  os.path.join(process_dir, variables["file-to-compare-to"]["value"]) 
    return {"differ": {"value": differ(input_file1, input_file2)}}

