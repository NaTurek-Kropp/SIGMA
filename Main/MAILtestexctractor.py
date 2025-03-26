import os
import imaplib
import email
import smtplib
import uuid
import sqlite3
from dotenv import load_dotenv
from email.message import EmailMessage
from email.header import decode_header
import random
import string
import Data

def generate_keycode():
    chars = string.ascii_letters + string.digits + "@#$&"
    return "".join(random.choices(chars, k=4))

# Load email credentials from .env
load_dotenv()
EMAIL = os.getenv("EMAIL_ACC")
PASSWORD = os.getenv("EMAIL_PASS")

# Database setup
DB_PATH = "tests.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tests (
        keycode TEXT PRIMARY KEY,
        filename TEXT,
        filedata BLOB
    )
""")
conn.commit()

def view_database():
    cursor.execute("SELECT * FROM tests")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def process_incoming_emails():
    """Check for emails, process attachments, and handle keycode assignments."""
    try:
        with imaplib.IMAP4_SSL("imap.gmail.com") as imap_server:
            imap_server.login(EMAIL, PASSWORD)
            imap_server.select("INBOX")
            
            # Search for all emails
            status, messages = imap_server.search(None, 'ALL')
            email_ids = messages[0].split()

            for email_id in email_ids:
                status, msg_data = imap_server.fetch(email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")
                        
                        # Process test uploads
                        if "TEST_UPLOAD" in subject.upper():
                            teacher_email = email.utils.parseaddr(msg.get("From"))[1]
                            for part in msg.walk():
                                if part.get_content_disposition() == "attachment":
                                    filename = part.get_filename()
                                    if filename:
                                        keycode = generate_keycode()
                                        filedata = part.get_payload(decode=True)
                                        try:
                                            cursor.execute("INSERT INTO tests (keycode, filename, filedata) VALUES (?, ?, ?)",
                                                           (keycode, filename, filedata))
                                            conn.commit()
                                            send_keycode_email(teacher_email, keycode)
                                        except sqlite3.Error as e:
                                            print(f"Database error: {e}")
                        # Process removal emails
                        elif subject.upper().startswith("REMOVE"):
                            parts = subject.split()
                            if len(parts) == 2:
                                keycode = parts[1]
                                remove_test(keycode)

                imap_server.store(email_id, "+FLAGS", "\\Deleted")

            imap_server.expunge()
    except Exception as e:
        print(f"Error processing emails: {e}")

def send_keycode_email(recipient, keycode):
    """Send an email with the generated keycode."""
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
            smtp_server.starttls()
            smtp_server.login(EMAIL, PASSWORD)
            msg = EmailMessage()
            msg["Subject"] = "Your Test Keycode"
            msg["From"] = EMAIL
            msg["To"] = recipient
            msg.set_content(f"Your keycode is: {keycode}")
            smtp_server.send_message(msg)
            print(f"Sent keycode {keycode} to {recipient}")
    except Exception as e:
        print(f"Error sending email: {e}")

def remove_test(keycode):
    """Delete a test from the database using a keycode."""
    try:
        cursor.execute("DELETE FROM tests WHERE keycode = ?", (keycode,))
        if cursor.rowcount:
            conn.commit()
            print(f"Test with keycode {keycode} removed.")
        else:
            print(f"No test found for keycode {keycode}.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def get_test_by_keycode(keycode):
    """Retrieve a test attachment using its keycode and process it."""
    try:
        cursor.execute("SELECT filename, filedata FROM tests WHERE keycode = ?", (keycode,))
        row = cursor.fetchone()
        if row:
            filename, filedata = row
            file_path = os.path.join(os.getcwd(), f"retrieved_{filename}")
            with open(file_path, "wb") as f:
                f.write(filedata)
            print(f"Retrieved {filename} and saved as {file_path}.")
            
            # Pass the file path to GetQuestionsDataFixed
            questions, answers = Data.GetQuestionsDataFixed(file_path)
            return questions, answers
        else:
            print("Invalid keycode!")
            return None, None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None, None

def NumOfQuestionsFromKeycode(keycode):
    """Retrieve a test using its keycode and count the number of questions."""
    try:
        cursor.execute("SELECT filename, filedata FROM tests WHERE keycode = ?", (keycode,))
        row = cursor.fetchone()
        if row:
            filename, filedata = row
            file_path = os.path.join(os.getcwd(), f"retrieved_{filename}")
            with open(file_path, "wb") as f:
                f.write(filedata)
            print(f"Retrieved {filename} and saved as {file_path}.")
            
            # Count questions
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            return len(lines) // 5
        else:
            print("Invalid keycode!")
            return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

if __name__ == "__main__":
    process_incoming_emails()
