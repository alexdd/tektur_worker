def transform_xml(variables):
    print ("transform xml called!")
    print ("xslt: "+variables["xslt"]["value"])
    print ("xslt-file: "+variables["xslt-file"]["value"])
    print ("source-file: "+variables["source-file"]["value"])
    print ("initial-template: "+variables["initial-template"]["value"])
    print ("destination-file: "+variables["destination-file"]["value"])
    print ("destination-serialization-method: "+variables["destination-serialization-method"]["value"])
    print ("parameters: "+str(variables["parameters"]["value"]))
    return ""
