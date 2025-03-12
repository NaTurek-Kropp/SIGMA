import random
import string

class Member:
    def __init__(self, name):
        self.name = name

class LobbyServer:
    def __init__(self):
        self.lobbies = {}
        self.lobby_id_counter = 1
        self.lobby_codes = {}

    def generate_lobby_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

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
        if lobby_id:
            return self.connect_member_to_lobby(lobby_id, member)
        else:
            return False

    def leave_lobby(self, lobby_id, member):
        if lobby_id in self.lobbies and member in self.lobbies[lobby_id]:
            self.lobbies[lobby_id].remove(member)
            return True
        else:
            return False

    def get_lobby_members(self, lobby_id):
        return self.lobbies.get(lobby_id, [])


# Example usage
if __name__ == "__main__":
    server = LobbyServer()
    lobby_id, lobby_code = server.create_lobby()
    print(f"Created lobby with ID: {lobby_id} and code: {lobby_code}")

    member = Member("Member1")
    if server.join_lobby_with_code(lobby_code, member):
        print(f"{member.name} joined lobby with code {lobby_code}")
    else:
        print(f"Failed to join lobby with code {lobby_code}")

    members = server.get_lobby_members(lobby_id)
    print(f"Members in lobby {lobby_id}: {[member.name for member in members]}")

    if server.leave_lobby(lobby_id, member):
        print(f"{member.name} left lobby {lobby_id}")
    else:
        print(f"Failed to leave lobby {lobby_id}")

    members = server.get_lobby_members(lobby_id)
    print(f"Members in lobby {lobby_id}: {[member.name for member in members]}")