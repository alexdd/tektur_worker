import os, tempfile
from subprocess import Popen, PIPE
from settings import SAXON_JAR
from errors import TaskError

def transform_xml(process_dir, variables):
    
    """This task runs an XSLT transformation calling Saxon via CLI.

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
