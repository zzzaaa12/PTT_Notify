# -*- coding: utf-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText

def send_notify_mail(subject, content):
    from_addr = ''
    to_addr = ''
    smtp_passwd = ''
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    if len(subject) and len(content):
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_addr, smtp_passwd)

        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = 'PTT Notify<' + from_addr + '>'
        msg['To'] = to_addr
        msg['Subject'] = Header(subject, 'utf-8').encode()

        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()

