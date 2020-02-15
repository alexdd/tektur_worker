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

import os, tempfile
from subprocess import Popen, PIPE
from settings import SAXON_JAR, JAVA_CMD, TIDY_CMD
from errors import TaskError

def transform_xml(process_dir, variables):
    
    """This task runs an XSLT transformation on an input file calling Saxon via CLI.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["initial-template"] -- The XSLT main template
        ["xslt-file"] -- The filename of the XSLT transformation file 
        ["xslt"] -- A string containing the XSLT Transformation instructions
        ["destination-file"] -- The name of the target file
        ["parameters"] -- a dictionary containing parameter settings passed to the transformation
    """
    
    source_file = os.path.join(process_dir, variables["source-file"]["value"])
    destination_file = os.path.join(process_dir, variables["destination-file"]["value"])
    os.makedirs(os.path.split(destination_file)[0], exist_ok=True)
    if variables["xslt-file"]["value"]:
        xslt_file = os.path.join(process_dir, variables["xslt-file"]["value"])
        delete_xslt_file = False
    else:
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".xsl", delete=False)
        f.write(variables["xslt"]["value"])
        f.close()
        xslt_file = f.name
        delete_xslt_file = True
    args = [
        JAVA_CMD,
        "-cp",
        SAXON_JAR,
        "net.sf.saxon.Transform",
        "-s:"+source_file,
        "-o:"+destination_file,
        "-xsl:"+xslt_file,
        ]
    if variables["initial-template"]["value"]:
        args.append("-it:"+variables["initial-template"]["value"])
    if variables["parameters"]["value"]:
        for saxon_param_strg in [key+"="+variables["parameters"]["value"][key] 
                             for key in variables["parameters"]["value"].keys()]:
            args.append(saxon_param_strg)
    args.append("workdir="+process_dir)
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == -1:
        raise TaskError("XSLT Error!", "Source: "+source_file+" XSLT: "+xslt_file)
    elif len(err) > 0:
        raise TaskError("XSLT Error!", err.decode())
    else:
        if delete_xslt_file:
            os.unlink(xslt_file)
    return {}

def batch_transform_xml(process_dir, variables):
    
    """This task runs a sequence of XSLT transformation on a set of input files calling Saxon via CLI.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["xslt-folder"] -- The name of the folder containing the XSLT files to process in sort order
        ["input-folder"] -- The name of the folder containing the input files 
        ["output-folder"] -- The name of the target folder; input folder structure will be replicated
        ["parameters"] -- a dictionary containing parameter settings passed to the transformation
    """

    outputf = os.path.join(process_dir, variables["output-folder"]["value"])
    input_folder = os.path.join(process_dir, variables["input-folder"]["value"])
    xslt_folder = os.path.join(process_dir, variables["xslt-folder"]["value"])
    os.mkdir(outputf)
    for file_name in os.listdir(input_folder): 
        if os.path.isdir(file_name):
            continue
        input_file =  os.path.join(input_folder, file_name)
        steps = os.listdir(xslt_folder)
        steps.sort()
        step = None  
        for step_file in steps:
            step = step_file.split("_")[0]
            output_folder = os.path.join(outputf,step)
            current_step = os.path.join(output_folder, file_name)
            os.makedirs(output_folder,exist_ok=True)
            args = [
                JAVA_CMD,
                "-cp",
                SAXON_JAR,
                "net.sf.saxon.Transform",
                "-s:"+input_file,
                "-o:"+current_step,
                "-xsl:"+xslt_folder+"/"+step_file,
            ]
            if variables["parameters"]["value"]:
                for saxon_param_strg in [key+"="+variables["parameters"]["value"][key] 
                                         for key in variables["parameters"]["value"].keys()]:
                    args.append(saxon_param_strg)
            args.append("workdir="+process_dir)
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()
            if p.returncode == -1:
                raise TaskError("XSLT Error!", "Source: "+file_name+" XSLT: "+step_file)
            elif len(err) > 0:
                raise TaskError("XSLT Error!", err.decode())
            input_file = current_step
    return {}
                
def batch_tidy_html(process_dir, variables):
    
    """This task batch converts html to xml using HTML Tidy via CLI.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["log-folder"] -- The name of the folder containing the HTML Tidy logfiles
        ["input-folder"] -- The name of the folder containing the input HTML files to tidy,
        ["output-folder"] -- The name of the resulting folder
        
    Note that Tidy needs some different parameters for the same thing, when run on Linux!
    """
    log_folder = os.path.join(process_dir, variables["log-folder"]["value"])
    input_folder = os.path.join(process_dir, variables["input-folder"]["value"])
    output_folder = os.path.join(process_dir, variables["output-folder"]["value"])
    os.makedirs(output_folder,exist_ok=True)
    os.makedirs(log_folder,exist_ok=True)

    for html_file in os.listdir(input_folder):
        if os.path.isdir(html_file):
            continue
        args = [
            TIDY_CMD,
            os.path.join(input_folder,html_file),
            "-n",
            "-asxml",
            "-o",
            "-c",
            "-q",
            "-"+variables["encoding"]["value"],
            "-f",
            log_folder+"/"+html_file.replace(".html",".txt"),
            "-o",
            os.path.join(output_folder,html_file.replace(".html",'.xml'))
        ] 
        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if p.returncode == -1:
            raise TaskError("TIDY Error!", "Source: "+html_file)
    return {}
