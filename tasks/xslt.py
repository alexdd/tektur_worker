import os, tempfile
from subprocess import Popen, PIPE
from settings import SAXON_JAR
from errors import TaskError

def transform_xml(process_dir, variables):
    
    source_file = os.path.join(process_dir, variables["source-file"]["value"])
    if len(variables["initial-template"]["value"]) > 0:
        initial_template = "-it:"+variables["initial-template"]["value"]
    else:
        initial_template = ""
    if len(variables["xslt-file"]["value"]) > 0:
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
        initial_template,
        "-s",
        source_file,
        "-o",
        os.path.join(process_dir, variables["destination-file"]["value"]),
        xslt_file,
        "workdir="+process_dir
        ]
    for saxon_param_strg in [key+"="+variables["parameters"]["value"][key] 
                             for key in variables["parameters"]["value"].keys()]:
        args.append('"'+saxon_param_strg+'"')
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == -1:
        raise TaskError("XSLT Error!", "Source: "+source_file+" XSLT: "+xslt_file)
    elif len(err) > 0:
        raise TaskError("XSLT Error!", err.decode())
    else:
        if delete_xslt_file:
            os.unlink(xslt_file)
