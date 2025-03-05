import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(toAdress, time, answers, name):
    fromAdress = 'your_email@example.com'
    password = 'pass'

    msg = MIMEMultipart()
    msg['From'] = fromAdress
    msg['To'] = toAdress
    msg['Subject'] = f'Wynik Testu {name[0], name[1]}'

    body = f"Time: {time}\nAnswers: {answers}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(fromAdress, password)
        text = msg.as_string()
        server.sendmail(fromAdress, toAdress, text)
        server.quit()
    except Exception as e:
        print(f"Error: {e}")
