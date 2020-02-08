import os, tempfile, glob
from subprocess import Popen, PIPE
from settings import SAXON_JAR
from errors import TaskError

def transform_xml(process_dir, variables):
    
    """This task runs an XSLT transformation on an input file calling Saxon via CLI.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictonary containing key-value pairs passed from Camunda
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
        "java",
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
        variables -- a dictonary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["xslt-folder"] -- The name of the folder containing the XSLT files to process in sort order
        ["input-folder"] -- The name of the folder containing the input files; 
                            THe folder must have subfolders containing the input files
        ["output-folder"] -- The name of the target folder; input folder structure will be replicated
        ["parameters"] -- a dictionary containing parameter settings passed to the transformation
    """

    outputf = os.path.join(process_dir, variables["output-folder"]["value"])
    inputf = os.path.join(process_dir, variables["input-folder"]["value"])
    xslt_folder = os.path.join(process_dir, variables["xslt-folder"]["value"])
    os.mkdir(outputf)
    glob_path = os.path.join(inputf,'*')
    for fpath in glob.glob(glob_path): 
        if os.path.isdir(fpath):
            continue
        file_name= os.path.basename(fpath)
        input_folder = os.path.dirname(os.path.realpath(fpath))
        input_file =  os.path.join(input_folder, file_name)
        steps = os.listdir(xslt_folder)
        steps.sort()
        step = None  
        for step_file in steps:
            step = step_file.split("_")[0]
            replname = input_folder.replace(inputf,outputf)
            output_folder = os.path.join(replname,step)
            current_step = os.path.join(output_folder, file_name)
            os.makedirs(output_folder,exist_ok=True)
            args = [
                "java",
                "-cp",
                SAXON_JAR,
                "net.sf.saxon.Transform",
                "-s:"+input_file,
                "-o:"+current_step,
                "-xsl:steps/"+step_file,
            ]
            if variables["parameters"]["value"]:
                for saxon_param_strg in [key+"="+variables["parameters"]["value"][key] 
                                         for key in variables["parameters"]["value"].keys()]:
                    args.append(saxon_param_strg)
            args.append("workdir="+process_dir)
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()
            if p.returncode == -1:
                raise TaskError("XSLT Error!", "Source: "+fpath+" XSLT: "+step_file)
            elif len(err) > 0:
                raise TaskError("XSLT Error!", err.decode())
            input_file = current_step
    return {}
        
def batch_validate_xml(process_dir, variables):
    
    """This task runs a Saxon XQuery on a list of XML files just in order to validate against a DTD; Calling Saxon via CLI.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictonary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["log-file"] -- The name of the log file containing the validation errors if any
        ["input-folder"] -- The name of the folder containing the input XML files to validate,
                            The folder must have subfolders containing the files
        ["valid"] -- Output bool variable containing the result of the validation process

    """

    log_file = os.path.join(process_dir, variables["log-file"]["value"])
    input_folder = os.path.join(process_dir, variables["input-folder"]["value"])
    f = open(log_file,"w")
    glob_path = os.path.join(input_folder,'*')
    for xml_file in glob.glob(glob_path):
        if os.path.isdir(xml_file):
            continue
        args = [
            "java",
            "-classpath",
            SAXON_JAR,
            "net.sf.saxon.Query",
            "-s:"+xml_file,
            "-qs:./THIS_DOES_NOT_EXIST",
            "-dtd:on"
            ]
        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        has_errors = False
        if p.returncode == -1:
            has_errors = True
            f.write("ERROR: Could not validate file: "+xml_file)
        elif len(err) > 0:
            has_errors = True
            f.write("ERROR: Could not validate file: "+xml_file+" Details: "+err.decode("utf8"))
        elif output != b'<?xml version="1.0" encoding="UTF-8"?>':
            has_errors = True
            f.write("NOT VALID "+xml_file)
    return {"valid": {"value": has_errors}}
