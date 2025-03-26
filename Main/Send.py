import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import Sub.Time as Time
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv() #env var

EMAIL = os.getenv("EMAIL_ACC")
PASSWORD = os.getenv("EMAIL_PASS")
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")
def send_email(toAdress, time, answers, name, title, klass):
    fromAdress = EMAIL
    password = PASSWORD

    msg = MIMEMultipart()
    msg['From'] = fromAdress
    msg['To'] = toAdress
    msg['Subject'] = f'Wynik Testu {klass}:{name}, {name} {get_current_date()}'

    time_total_seconds = sum(item for item in time)
    hours, remainder = divmod(time_total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_total = f"{hours}:{minutes}:{seconds} hh-mm-ss"
    body = f"Całkowity Czas: {time_total}\n\n"
    i = 0
    for el in answers:
        minutes, seconds = divmod(time[i], 60)
        body += f"Pytanie {i + 1}: Odp: {el}, Czas: {minutes}:{seconds}\n"
        i+=1

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
