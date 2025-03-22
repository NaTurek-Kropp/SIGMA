import random
import string

class Member:
    def __init__(self, name):
        self.name = name
        self.answers = []

class LobbyServer:
    def __init__(self):
        self.lobbies = {}
        self.lobby_codes = {}
        self.game_started = {}
        self.rounds = {}
        self.lobby_id_counter = 1

    def generate_lobby_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
    
    def create_lobby(self):
        lobby_id = self.lobby_id_counter
        lobby_code = self.generate_lobby_code()
        
        self.lobbies[lobby_id] = []
        self.lobby_codes[lobby_code] = lobby_id
        self.rounds[lobby_id] = 0
        self.game_started[lobby_id] = False
        
        self.lobby_id_counter += 1
        return lobby_id, lobby_code
    
    def get_lobby_id_from_code(self, lobby_code):
        return self.lobby_codes.get(lobby_code)
    
    def connect_member_to_lobby(self, lobby_id, member):
        if lobby_id in self.lobbies and member.name not in [m.name for m in self.lobbies[lobby_id]]:
            self.lobbies[lobby_id].append(member)
            return True
        return False
    
    def join_lobby_with_code(self, lobby_code, member_name):
        lobby_id = self.get_lobby_id_from_code(lobby_code)
        if lobby_id is not None:
            return self.connect_member_to_lobby(lobby_id, Member(member_name))
        return False
    
    def start_game(self, lobby_id):
        if lobby_id in self.lobbies and not self.game_started[lobby_id]:
            self.game_started[lobby_id] = True
            return True
        return False
    
    def is_game_started(self, lobby_id):
        return self.game_started.get(lobby_id, False)
    
    def set_round(self, lobby_id):
        if lobby_id in self.lobbies:
            self.rounds[lobby_id] += 1
            return True
        return False
    
    def submit_answer(self, lobby_id, member_name, answer):
        if lobby_id in self.lobbies:
            for member in self.lobbies[lobby_id]:
                if member.name == member_name:
                    member.answers.append(answer)
                    return True
        return False
    
    def all_members_submitted(self, lobby_id):
        current_round = self.rounds.get(lobby_id, 0)
        return all(len(member.answers) >= current_round for member in self.lobbies.get(lobby_id, []))
    
    def leave_lobby(self, lobby_id, member_name):
        if lobby_id in self.lobbies:
            self.lobbies[lobby_id] = [m for m in self.lobbies[lobby_id] if m.name != member_name]
            return True
        return False
    
    def get_lobby_members(self, lobby_id):
        return [member.name for member in self.lobbies.get(lobby_id, [])]
    
    def get_lobby_member_objects(self, lobby_id):
        return self.lobbies.get(lobby_id, [])


def test_create_lobby_and_start_game():
    server = LobbyServer()
    
    lobby_id, lobby_code = server.create_lobby()
    assert lobby_id is not None and lobby_code is not None, "Lobby creation failed!"
    print("Lobby created with ID:", lobby_id, "Code:", lobby_code)

    assert server.join_lobby_with_code(lobby_code, "A"), "Failed to add A!"
    assert server.join_lobby_with_code(lobby_code, "B"), "Failed to add B!"
    assert server.join_lobby_with_code(lobby_code, "I"), "Failed to add I!"

    game_started = server.start_game(lobby_id)
    assert game_started, "Failed to start the game!"
    print("Game started successfully!")
    
    assert server.is_game_started(lobby_id), "Game should be started but is not!"
    print("Game start status verified!")
    
    server.set_round(lobby_id)
    
    assert server.submit_answer(lobby_id, "A", "B"), "Failed to submit answer for A!"
    assert server.submit_answer(lobby_id, "B", "B"), "Failed to submit answer for B!"
    
    print("All members submitted:", server.all_members_submitted(lobby_id))
    print("Lobby members:", server.get_lobby_member_objects(lobby_id))

#test_create_lobby_and_start_game()