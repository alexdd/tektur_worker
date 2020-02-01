import os, smtplib, mimetypes
from settings import EMAIL_ADDRESS, EMAIL_SERVER, EMAIL_PASSWORD, EMAIL_USER
from email.message import EmailMessage
from errors import TaskError

def send_mail(process_dir, variables):
    
    """This task sends an eMail.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictonary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["to"] -- The recepient's email address
        ["subject"] -- The subject line of the email
        ["body"] -- The text body of the eMail
        ["attachment"] -- the path of the file (ZIP) to be attached
        ["attachedName"] -- the name of the attachment in the eMail
    """

    msg = EmailMessage()
    msg['Subject'] = variables["subject"]["value"]
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = variables["to"]["value"]
    msg.set_content(variables["body"]["value"])
    if variables["attachment"]["value"]:
        attachment = os.path.join(process_dir, variables["attachment"]["value"])
        try:
            ctype, encoding = mimetypes.guess_type(attachment)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(attachment, 'rb') as fp:
                data = fp.read()
                msg.add_attachment(data,
                                   maintype=maintype,
                                   subtype=subtype,
                                   filename=variables["attachedName"]["value"])
        except Exception as e:
            raise TaskError("MAIL attachment error!",str(e) )
    try:
        with smtplib.SMTP(EMAIL_SERVER) as s:
            s.login(EMAIL_USER, EMAIL_PASSWORD)
            s.send_message(msg) 
    except Exception as e:
        raise TaskError("MAIL send error!",str(e) )
    return {}
