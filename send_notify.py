# -*- coding: utf-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText

FROM_ADDR = ''
TO_ADDR = ''
SMTP_PASSWD = ''
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def send_notify_mail(subject, content):
    if len(subject) and len(content):
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_ADDR, SMTP_PASSWD)

        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = 'PTT Notify<' + FROM_ADDR + '>'
        msg['To'] = TO_ADDR
        msg['Subject'] = Header(subject, 'utf-8').encode()

        server.sendmail(FROM_ADDR, TO_ADDR, msg.as_string())
        server.quit()

