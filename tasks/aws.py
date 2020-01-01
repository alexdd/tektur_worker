import os, boto3
from errors import TaskError

def s3_get(process_dir, variables):
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
    print ("s3 list called!")
    print ("bucket: "+variables["bucket"]["value"])
    print ("key: "+variables["key"]["value"])
    print ("Sort: "+variables["sort"]["value"])
    print ("Sort by: "+variables["sort-by"]["value"])

def s3_put(process_dir, variables):
    print ("s3 put called!")
    print ("bucket: "+variables["bucket"]["value"])
    print ("key: "+variables["key"]["value"])
    print ("filename: "+variables["filename"]["value"])

