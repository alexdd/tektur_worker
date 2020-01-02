import os, boto3, re
from errors import TaskError

def s3_get(process_dir, variables):
    
    """This task downloads a file from a S3 bucket.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictonary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["filename"] -- The name of the file to store the content to
        ["key"] -- The name of the S3 object to download  
        ["bucket"] -- The name of the S3 bucket
    """

    s3 = boto3.client('s3')
    path = os.path.join(process_dir, variables["filename"]["value"])
    key = variables["key"]["value"]
    bucket = variables["bucket"]["value"]
    try:
        with open(path, 'wb') as f:
            s3.download_fileobj(bucket, key, f)
    except Exception as e:
        raise TaskError("Cannot get S3 object!", str(e)+": "+bucket+"/"+key)

def s3_list(process_dir, variables):

    """This task lists object contained in a S3 bucket.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictonary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["bucket"] -- The name of the S3 bucket
        ["key"] -- A regex defining the object names to list 
    """
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(variables["bucket"]["value"])
    regex = re.compile(variables["key"]["value"])
    try:
        matches = [obj_name for obj_name in bucket.objects.all() if re.match(regex, obj_name)]
    except Exception as e:
        raise TaskError("Cannot list S3 objects!", str(e)+": "+str(bucket))
    print("s3 list calles! "+str(matches))
    
def s3_put(process_dir, variables):

    """This task puts a file into a S3 bucket.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictonary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["filename"] -- The name of the file to put into the bucket
        ["bucket"] -- The name of the bucket
        ["key"] -- The name of the target object on S3
    """
    
    s3 = boto3.client('s3')
    path = os.path.join(process_dir, variables["filename"]["value"])
    key = variables["key"]["value"]
    bucket = variables["bucket"]["value"]
    try:
        with open(path, "rb") as f:
            s3.upload_fileobj(f, bucket, key)
    except Exception as e:
        raise TaskError("Cannot put S3 object!", str(e)+": "+bucket+"/"+key)
