import random
import string

class Member:
    def __init__(self, name):
        self.name = name
        self.aswers = []
        
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
        if lobby_id and not any(m.name == member.name for m in self.lobbies.get(lobby_id, [])):
            return self.connect_member_to_lobby(lobby_id, member)
        else:
            return False
        
    def start_game(self, lobby_id):
        if lobby_id in self.lobbies:
            self.questions[lobby_id] = []
            self.gameStarted[lobby_id] = True
            return True
        else:
            return False
        
    def is_game_started(self, lobby_id):
        print(self.lobbies)
        if lobby_id in self.lobbies:
            print(self.gameStarted.get(lobby_id))
            return self.gameStarted.get(lobby_id)
        else:
            return BaseException("No such lobby id!")
    
    def submit_answer(self, lobby_id, member_name, answer):
        if lobby_id in self.lobbies:
            for member in self.lobbies[lobby_id]:
                if member.name == member_name:
                    member.answers.append(answer)
                    return True
        return False
    
    def all_members_submitted(self, lobby_id):
        if lobby_id in self.lobbies and lobby_id in self.round:
            current_round = self.round[lobby_id]
            for member in self.lobbies[lobby_id]:
                if len(member.answers) != current_round:
                    return False
            return True
        return False

    def leave_lobby(self, lobby_id, member):
        if lobby_id in self.lobbies and member in self.lobbies[lobby_id]:
            self.lobbies[lobby_id].remove(member)
            return True
        else:
            return False

    def get_lobby_members(self, lobby_id):
        return self.lobbies.get(lobby_id, [])
    

