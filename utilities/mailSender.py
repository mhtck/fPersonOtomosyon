import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

def sendMail(toMailAdress):
    
    mesaj = MIMEMultipart()
    
    mesaj["from"] = "example@example.com" #current mail
    mesaj["to"] = toMailAdress
    mesaj["subject"] = "Onay Maili"

    num = random.randrange(1000,9999)
    yazi = "Merhaba sayfaya giriş için şifreniz: {}".format(num)
    mesaj_yapisi = MIMEText(yazi, "plain")
    mesaj.attach(mesaj_yapisi)
    try:
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login("example@example.com", "qwer123@")
        mail.sendmail(mesaj["from"], mesaj["to"], mesaj.as_string())
        print("Mail gönderildi")
        mail.close()
        return (True,num)
    except:
        return (False,num)


