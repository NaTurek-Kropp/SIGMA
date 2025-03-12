import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import Data
import random
import Sub.Time as Time
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../Main")))
from ProjectData import Settings

load_dotenv() #env var

EMAIL = os.getenv("EMAIL_ACC")
PASSWORD = os.getenv("EMAIL_PASS")

def send_email(toAdress, time, answers, name):
    fromAdress = EMAIL
    password = PASSWORD

    msg = MIMEMultipart()
    msg['From'] = fromAdress
    msg['To'] = toAdress
    msg['Subject'] = f'Wynik Testu {name[0]} {name[1]}'

    body = f"Time: {time}\nAnswers: {answers}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromAdress, password)
        text = msg.as_string()
        server.sendmail(fromAdress, toAdress, text)
        server.quit()
    except Exception as e:
        print(f"Error: {e}")
