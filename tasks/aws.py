import boto3

def s3_get(process_dir, variables):
    print ("s3 get called!")
    print ("bucket: "+variables["bucket"]["value"])
    print ("key: "+variables["key"]["value"])
    print ("URL: "+variables["url"]["value"])
    print ("filename: "+variables["filename"]["value"])
    print ("profile: "+variables["profile"]["value"])

def s3_list(process_dir, variables):
    print ("s3 list called!")
    print ("bucket: "+variables["bucket"]["value"])
    print ("key: "+variables["key"]["value"])
    print ("URL: "+variables["url"]["value"])
    print ("Sort: "+variables["sort"]["value"])
    print ("Sort by: "+variables["sort-by"]["value"])
    print ("profile: "+variables["profile"]["value"])

def s3_put(process_dir, variables):
    print ("s3 put called!")
    print ("bucket: "+variables["bucket"]["value"])
    print ("key: "+variables["key"]["value"])
    print ("URL: "+variables["url"]["value"])
    print ("filename: "+variables["filename"]["value"])
    print ("profile: "+variables["profile"]["value"])

