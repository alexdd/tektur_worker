def http_request(process_dir, variables):
    print ("http request called!")
    print ("method: "+variables["method"]["value"])
    print ("host: "+variables["host"]["value"])
    print ("port: "+variables["port"]["value"])
    print ("endpoint: "+variables["endpoint"]["value"])
    print ("queryParameters: "+str(variables["queryParameters"]["value"]))
    print ("contentType: "+variables["contentType"]["value"])
    print ("requestBody: "+variables["requestBody"]["value"])
    print ("requestBodyFilename: "+variables["requestBodyFilename"]["value"])
    print ("responseBodyFilename: "+variables["responseBodyFilename"]["value"])
    return {}
