import requests
import threading
import time
from ProjectData import Settings
import Send

online = False
isInLobby = False
lobby_id = None
lobby_code = None
lobby_data = None
lobby_thread = None

API = "http://127.0.0.1:5000" 
#"https://powarznastrona.pythonanywhere.com"

def isOnline(isonline: bool):
    global online
    online = isonline

def create_lobby():
    global lobby_id, lobby_code, lobby_data, lobby_thread, isInLobby
    isInLobby = True
    response = requests.post(f'{API}/create_lobby')
    if response.status_code == 201:
        lobby_data = response.json()
        lobby_id = lobby_data['lobby_id']
        lobby_code = lobby_data['lobby_code']
        print(f"Lobby created with ID: {lobby_id} and code: {lobby_code}")
        lobby_thread = threading.Thread(target=check_lobby_updates, daemon=True)
        lobby_thread.start()
    else:
        print("Failed to create lobby")

def get_lobby_members():
    response = requests.get(f'{API}/get_lobby_members', params={'lobby_id': lobby_id})
    return response.json().get('members', [])

def setRound():
    data = {'lobby_id': lobby_id}
    requests.post(f'{API}/setRound', json=data)

def start_game_online():
    data = {'lobby_id': lobby_id}
    response = requests.post(f'{API}/start_game', json=data)
    if response.status_code == 200:
        print("Online game started successfully.")
    else:
        print("Failed to start online game.")

def check_submit_updates():
    while True:
        response = requests.get(f'{API}/all_members_submitted', params={'lobby_id': lobby_id})
        if response.status_code == 200 and response.json().get('all_submitted'):
            from Quiz import nextQuestion
            nextQuestion()
        time.sleep(5)

def check_lobby_updates():
    global lobby_data, isInLobby
    while isInLobby:
        response = requests.get(f'{API}/get_lobby_members', params={'lobby_id': lobby_id})
        if response.status_code == 200:
            new_lobby_data = response.json()
            if new_lobby_data != lobby_data:
                lobby_data = new_lobby_data
                from Quiz import createSurface
                createSurface("update-lobby")
        time.sleep(5)

def sendEmails():
    response = requests.get(f'{API}/get_lobby_member_objects', params={'lobby_id': lobby_id})
    if response.status_code == 200:
        for member in response.json().get('members', []):
            Send.send_email(Settings.GetSetting("email-adress"), [], member.get('answers', []), member.get('name', ''))
    else:
        print("Failed to retrieve lobby member objects for emails.")
