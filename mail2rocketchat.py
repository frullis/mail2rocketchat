import imaplib
import email
import pprint
import sys
import requests
import smtplib

imap_host = 'mail3.example.org'
imap_user = 'username'
imap_pass = '***'

from_addr = "debug@5july.org"
to_addr = "markus@5july.org"


# connect to host using SSL
imap = imaplib.IMAP4_SSL(imap_host)

## login to server
try:
    imap.login(imap_user, imap_pass)
except:
    print (sys.exc_info()[1])

imap.select('Inbox')

http_headers = {'Content-type': 'application/json',
        'user-agent': 'python script'}

tmp, data = imap.search(None, '(SEEN)')
for num in data[0].split():
    tmp, data = imap.fetch(num, '(RFC822)')
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            print("From:", msg['From'])
            print("Subject:", msg['Subject'])
            subject = msg['Subject']
            email_from = msg['From']
    msg = email.message_from_bytes(data[0][1])
    #print(data[0][1])
    print("MSG:")
    print(msg.get_payload())
    print('Message: {0}\n'.format(num))
    #pprint.pprint(data[0][1])
    #break

    json_payload = {"username":"rootmails","text": subject,"attachments":[{"title":email_from,"title_link":"https://rocket.chat","text":"Rocket.Chat,"+ msg.get_payload(),"image_url":"https://rocket.chat/images/mockup.png","color":"#764FA5"}]}
    try:
        req = requests.post("https://m.example.org/hooks/s9TpCKujKQYwuuYLM/A5b6vBt4gNVsijc7asBnxHuoojFkwjzBgG8Na3RwSr3cm95Q", headers=http_headers, json=json_payload)
    except requests.exceptions.RequestException:
        mail = smtplib.SMTP('localhost')
        msg = "From: DebugCentral <"+from_addr+">\r\nTo: Root <"+to_addr+">\r\nSubject: Email2Rocketchat failed\r\n\nWarning Email to rocket chatfailed\r\n"
        mail.sendmail(from_addr, to_addr, msg)
        mail.quit()


        print("Connection Error")

imap.close()
