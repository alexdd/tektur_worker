def send_mail(variables):
    print ("send mail called!")
    print ("to: "+variables["to"]["value"])
    print ("subject: "+variables["subject"]["value"])
    print ("body: "+variables["body"]["value"])
    print ("attachment: "+variables["attachment"]["value"])
    return ""
