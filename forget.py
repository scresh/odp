from auto_login import auto_login
import smtplib

server = smtplib.SMTP(auto_login('mail_smtp'), auto_login('mail_port'))
server.ehlo()
server.starttls()
server.ehlo()
server.login(auto_login('mail_user'), auto_login('mail_passwd'))
msg = "ur message"
server.sendmail(auto_login('mail_user'), "screshowski@gmail.com", msg)
server.quit()
