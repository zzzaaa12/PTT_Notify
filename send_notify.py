import smtplib

def send_notify_mail(subject, message):
    fromaddr = ''
    toaddr = ''
    smtp_passwd = ''
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    if len(subject) and len(message):
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(fromaddr, smtp_passwd)

        send_msg = 'Subject: ' + subject + '\r\n' + 'From: ' + fromaddr + '\r\nTo: ' + toaddr + '\r\n\r\n' + message
        server.sendmail(fromaddr, toaddr, send_msg)
        server.quit()

