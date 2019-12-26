

def file_zip(variables):
    print ("zip called!")
    print ("output: "+variables["zipFilename"]["value"])
    print ("input: "+variables["inputFilenames"]["value"])
    return ""

def file_unzip(variables):
    print ("unzip called!")
    print ("input: "+variables["zipFilename"]["value"])
    print ("output: "+variables["outputFolder"]["value"])
    return ""


