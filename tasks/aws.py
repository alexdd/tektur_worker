#    Tektur Worker - Camuda eternal task executor for ETL processes 
#    Copyright (C) 2020  Alex Düsel, tekturcms@gmail.com

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

import os, boto3, re, json
from errors import TaskError

def s3_get(process_dir, variables):
    
    """This task downloads a file from a S3 bucket.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["filename"] -- The name of the file to store the content to
        ["key"] -- The name of the S3 object to download  
        ["bucket"] -- The name of the S3 bucket
    """

    filename = variables["filename"]["value"]
    if not filename:
        raise TaskError("AWS Error! Filename required")
    
    s3 = boto3.client('s3')
    path = os.path.join(process_dir, filename)
    key = variables["key"]["value"]
    bucket = variables["bucket"]["value"]
    try:
        with open(path, 'wb') as f:
            s3.download_fileobj(bucket, key, f)
    except Exception as e:
        raise TaskError("AWS Error! Cannot get S3 object!", str(e)+": "+bucket+"/"+key)
    return {}

def s3_list(process_dir, variables):

    """This task lists objects contained in a S3 bucket. It return a dictonary 
       with format {"objects": "value" : [list of object names]

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["bucket"] -- The name of the S3 bucket
        ["key"] -- A regex defining the object names to list 
        ["objects"] -- Output variable containing the list of 
                       filenames of the objects to be retrieved       
    """
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(variables["bucket"]["value"])
    regex = re.compile(variables["key"]["value"])
    try:
        return {"objects": {"value": [bucket.key for bucket in bucket.objects.all() 
                                                            if re.match(regex, bucket.key)]}}
    except Exception as e:
        raise TaskError("AWS Error! Cannot list S3 objects!", str(e)+": "+str(bucket))
    
def s3_put(process_dir, variables):

    """This task puts a file into a S3 bucket.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["filename"] -- The name of the file to put into the bucket
        ["bucket"] -- The name of the bucket
        ["key"] -- The name of the target object on S3
    """
    
    s3 = boto3.client('s3')
    path = os.path.join(process_dir, variables["filename"]["value"])
    key = variables["key"]["value"]
    if variables["location"]["value"] == 'process': 
        path = os.path.join(process_dir, variables["filename"]["value"])
    else:
        path = os.path.join(variables["filename"]["value"])
    bucket = variables["bucket"]["value"]
    try:
        with open(path, "rb") as f:
            s3.upload_fileobj(f, bucket, key)
    except Exception as e:
        raise TaskError("AWS Error! Cannot put S3 object!", str(e)+": "+bucket+"/"+key)
    return {}