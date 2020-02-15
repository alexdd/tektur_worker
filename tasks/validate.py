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
from settings import SAXON_JAR, JAVA_CMD, SCHEMATRON_DIR
from errors import TaskError

def batch_validate_xml(process_dir, variables):
    
    """This task runs a Saxon XQuery on a list of XML files just in order to validate against a DTD; Calling Saxon via CLI.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["log-file"] -- The name of the log file containing the validation errors if any
        ["input-folder"] -- The name of the folder containing the input XML files to validate,
        ["valid"] -- Output bool variable containing the result of the validation process

    """  

    log_file = os.path.join(process_dir, variables["log-file"]["value"])
    input_folder = os.path.join(process_dir, variables["input-folder"]["value"])
    f = open(log_file,"w")
    for xml_file in os.listdir(input_folder):
        if os.path.isdir(xml_file):
            continue
        args = [
            JAVA_CMD,
            "-classpath",
            SAXON_JAR,
            "net.sf.saxon.Query",
            "-s:"+os.path.join(input_folder,xml_file),
            "-qs:./THIS_DOES_NOT_EXIST",
            "-dtd:on"
            ]
        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        valid = True
        if p.returncode == -1:
            has_errors = False
            f.write("ERROR: Could not validate file: "+xml_file)
        elif len(err) > 0:
            has_errors = False
            f.write("ERROR: Could not validate file: "+xml_file+" Details: "+err.decode("utf8"))
        elif output != b'<?xml version="1.0" encoding="UTF-8"?>':
            has_errors = False
            f.write("NOT VALID "+xml_file)
    return {"valid": {"value": has_errors}}

def call_schematron_stylesheets(source, target, xslt):
    
    args = [
        JAVA_CMD,
        "-cp",
        SAXON_JAR,
        "net.sf.saxon.Transform",
        "-s:"+source,
        "-o:"+target,
        "-xsl:"+xslt,
        ]
    
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == -1:
        raise TaskError("Schematron Create Error!", "Source: "+source_file+" XSLT: "+xslt_file)
    elif len(err) > 0:
        raise TaskError("Schematron Create Error!", err.decode())
    
def generate_schematron_xslt(process_dir, variables):
    
    """This task creats the Schematron XSLT file from a Schematron rules file.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["schematron-file"] -- The name of the file containing the schematron rules if not declared inline,
        ["schematron"] -- if there is no file, than the inline Camunda field will be considered
        ["schematron-xslt"] -- The name of the resulting XSLT file
    """  

    if variables["schematron-file"]["value"]:
        schematron_file = os.path.join(process_dir, variables["schematron-file"]["value"])
        delete_schematron_file = False
    else:
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".xsl", delete=False)
        f.write(variables["schematron"]["value"])
        f.close()
        schematron_file = f.name
        delete_schematron_file = True
    
    include_tmp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".xsl", delete=False)
    expand_tmp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".xsl", delete=False)
    
    call_schematron_stylesheets(
        schematron_file, 
        include_tmp_file.name, 
        os.path.join(SCHEMATRON_DIR, "iso_dsdl_include.xsl"))

    call_schematron_stylesheets(
        include_tmp_file.name, 
        expand_tmp_file.name, 
        os.path.join(SCHEMATRON_DIR, "iso_abstract_expand.xsl"))

    call_schematron_stylesheets(
        expand_tmp_file.name, 
        os.path.join(process_dir, variables["schematron-xslt"]["value"]), 
        os.path.join(SCHEMATRON_DIR, "iso_svrl_for_xslt2.xsl"))
    
    if delete_schematron_file:
        os.unlink(schematron_file)
    return {}
    
    
