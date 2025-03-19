import random
import string

class Member:
    def __init__(self, name):
        self.name = name
        self.answers = []
        
class LobbyServer:
    def __init__(self):
        self.lobbies = {}
        self.lobby_id_counter = 1
        self.lobby_codes = {}
        self.questions = {}
        self.gameStarted = {}
        self.round = {}

    def generate_lobby_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def get_lobby_id_from_code(self, lobby_code):
        return self.lobby_codes.get(lobby_code)
    
    def create_lobby(self):
        lobby_id = self.lobby_id_counter
        lobby_code = self.generate_lobby_code()
        self.lobbies[lobby_id] = []
        self.lobby_codes[lobby_code] = lobby_id
        self.lobby_id_counter += 1
        return lobby_id, lobby_code

    def connect_member_to_lobby(self, lobby_id, member):
        if lobby_id in self.lobbies:
            self.lobbies[lobby_id].append(member)
            return True
        else:
            return False

    def join_lobby_with_code(self, lobby_code, member):
        lobby_id = self.lobby_codes.get(lobby_code)
        if lobby_id and not any(m.name == member for m in self.lobbies.get(lobby_id, [])):
            return self.connect_member_to_lobby(lobby_id, Member(member))
        else:
            return False
        
    def start_game(self, lobby_id):
        if lobby_id in self.lobbies:
            self.questions[lobby_id] = []
            print("Started game!")
            self.gameStarted[lobby_id] = True
            return True
        else:
            return False
        
    def is_game_started(self, lobby_id):
        id = int(lobby_id)
        print(self.gameStarted.get(id))
        return self.gameStarted.get(id)
    
    def set_round(self, lobby_id, value):
        self.round[lobby_id] = value
        return True
    
    def submit_answer(self, lobby_id, member_name, answer):
        if lobby_id in self.lobbies:
            print(self.lobbies[lobby_id])
            for member in self.lobbies[lobby_id]:
                if member.name == member_name:
                    member.answers.append(answer)
                    return True
        return False
    
    def all_members_submitted(self, lobby_id):
        current_round = self.round[lobby_id]
        for member in self.lobbies[lobby_id]:
            if len(member.answers) != current_round:
                return False
        return True

    def leave_lobby(self, lobby_id, member):
        if not lobby_id > self.lobby_id_counter and not lobby_id < 1 and member in self.lobbies[lobby_id]:
            self.lobbies[lobby_id].remove(member)
            return True
        else:
            return False

    def get_lobby_members(self, lobby_id):
        members = self.lobbies.get(lobby_id, [])

        return [member.name for member in members]
    
    def get_lobby_member_objects(self, lobby_id):
        return self.lobbies.get(lobby_id, [])
    

def test_create_lobby_and_start_game():
    server = LobbyServer()
    
    lobby_id, lobby_code = server.create_lobby()
    assert lobby_id is not None and lobby_code is not None, "Lobby creation failed!"
    print(f"Lobby created with ID: {lobby_id}, Code: {lobby_code}")

    server.join_lobby_with_code(lobby_code, "A")
    
    server.join_lobby_with_code(lobby_code, "B")

    game_started = server.start_game(lobby_id)
    assert game_started, "Failed to start the game!"
    print("Game started successfully!")
    
    print(lobby_id)
    assert server.is_game_started(lobby_id), "Game should be started but is not!"
    print("Game start status verified!")
    
    server.set_round(lobby_id, 1)

    server.submit_answer(lobby_id, "A", "B")
    
    print(server.all_members_submitted(lobby_id))
test_create_lobby_and_start_game()
