import email
import imaplib
import os
from datetime import datetime

import names
import pandas as pd

from conf.credentials import email_address, email_password, imap_url

user = email_address
password = email_password
imap_url = imap_url


def get_body(msg):
    """
    :param msg:
    :return:
    """
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def search(key, value, connection):
    """
    :rtype: object
    :param key:
    :param value:
    :param connection:
    :return:
    """
    result, data = connection.search(None, key, '"{}"'.format(value))
    return data


def get_emails(result_bytes) -> object:
    """
    :rtype: object
    """
    msgs = []
    for num in result_bytes[0].split():
        typ, data = connection.fetch(num, '(RFC822)')
        msgs.append(data)

    return msgs


connection = imaplib.IMAP4_SSL(imap_url)

connection.login(user, password)

connection.select('Inbox')

searchEmail = 'ashu.yadav@reliason.com '

msgs = get_emails(search('FROM', searchEmail, connection))

now = datetime.now()
dt_string = now.strftime("%d_%m_%Y%H_%M_%S")

emailData = []


def download_attachments(msg):
    for part in msg.walk():
        content_disposition = str(part.get("Content-Disposition"))
        if "attachment" in content_disposition:
            filename = part.get_filename()
            if filename:
                if not os.path.isdir('./Attachments/{}/'.format(email.utils.parseaddr(email_from)[1])):
                    os.mkdir('./Attachments/{}/'.format(email.utils.parseaddr(email_from)[1]))
                filepath = os.path.join('./Attachments/{}/'.format(email.utils.parseaddr(email_from)[1]),
                                        filename)
                open(filepath, "wb").write(part.get_payload(decode=True))


for response_part in msgs[::-1]:
    for sent in response_part:

        if isinstance(sent, tuple):
            dicts = {} # empty dict
            msg = email.message_from_string(sent[1].decode('utf-8'))
            email_subject = msg['subject']
            email_from = msg['from']
            email_body = get_body(msg).decode()
            if msg.is_multipart():  # to check if attachment exists
                download_attachments(msg)

            dicts['From'] = email_from
            dicts['Subject'] = email_subject
            dicts['Body'] = email_body
            emailData.append(dicts)
            print('-------------------')

df = pd.DataFrame(emailData)
name = names.get_last_name()
if not os.path.isdir('./output/{}/'.format(searchEmail)):
    os.mkdir('./output/{}/'.format(searchEmail))
df.to_excel("./output/" + searchEmail + "/" + searchEmail + dt_string + '.xls')
df.to_csv("./output/" + searchEmail + "/" + searchEmail + dt_string + '.csv')
