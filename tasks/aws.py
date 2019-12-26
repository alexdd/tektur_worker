
def s3_get(variables):
    print ("s3 get called!")
    print ("bucket: "+variables["bucket"]["value"])
    print ("key: "+variables["key"]["value"])
    print ("URL: "+variables["url"]["value"])
    print ("filename: "+variables["filename"]["value"])
    print ("profile: "+variables["profile"]["value"])
    return ""

def s3_list(variables):
    print ("s3 list called!")
    print ("bucket: "+variables["bucket"]["value"])
    print ("key: "+variables["key"]["value"])
    print ("URL: "+variables["url"]["value"])
    print ("Sort: "+variables["sort"]["value"])
    print ("Sort by: "+variables["sort-by"]["value"])
    print ("profile: "+variables["profile"]["value"])
    return ""

def s3_put(variables):
    print ("s3 put called!")
    print ("bucket: "+variables["bucket"]["value"])
    print ("key: "+variables["key"]["value"])
    print ("URL: "+variables["url"]["value"])
    print ("filename: "+variables["filename"]["value"])
    print ("profile: "+variables["profile"]["value"])
    return ""

