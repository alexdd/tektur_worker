#    Tektur Worker - Camuda external task executor for ETL processes 
#    Copyright (C) 2020 - 2025  Alex Duesel, tekturcms@gmail.com

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

import os, smtplib, mimetypes
from settings import EMAIL_ADDRESS, EMAIL_SERVER, EMAIL_PASSWORD, EMAIL_USER
from email.message import EmailMessage
from errors import TaskError

def send_mail(process_dir, variables):
    
    """This task sends an eMail.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
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
