import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import Data
import random
import Sub.Time as Time

ans = Data.Answers()
answers = ['A', 'B', 'C', 'D']
for _ in range(10):
    ans.AppendAnswer(random.choice(answers))

def send_email(toAdress, time, answers, name):
    fromAdress = 'bardzo.powarzny.email321@gmail.com'
    password = 'puga rvvs qlrs ppef'

    msg = MIMEMultipart()
    msg['From'] = fromAdress
    msg['To'] = toAdress
    msg['Subject'] = f'Wynik Testu {name[0], name[1]}'

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

send_email('mikolajmaczewski298@gmail.com',Time.TimeStamps(), ans.Answers(), "Barte")



