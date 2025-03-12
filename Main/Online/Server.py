from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from Lobby import LobbyServer, Member
from flask_cors import CORS 

app = Flask(__name__)
bcrypt = Bcrypt(app)
server = LobbyServer()
CORS(app) #kurwa mać

@app.route('/create_lobby', methods=['POST'])
def create_lobby():
    lobby_id, lobby_code = server.create_lobby()
    return jsonify({'lobby_id': lobby_id, 'lobby_code': lobby_code}), 201


@app.route('/get_lobby_id_from_code', methods=['GET'])
def get_lobby_id_from_code():
    lobby_code = request.args.get('lobby_code')

    if not lobby_code:
        return jsonify({'message': 'Lobby code is required'}), 400

    lobby_id = server.get_lobby_id_from_code(lobby_code)
    if lobby_id is not None:
        return jsonify({'lobby_id': lobby_id}), 200
    else:
        return jsonify({'message': 'Invalid lobby code'}), 400
    
@app.route('/join_lobby', methods=['POST'])
def join_lobby():
    data = request.get_json()
    lobby_code = data.get('lobby_code')
    member_name = data.get('member_name')

    if not lobby_code or not member_name:
        return jsonify({'message': 'Lobby code and member name are required'}), 400

    member = Member(member_name)
    if server.join_lobby_with_code(lobby_code, member):
        return jsonify({'message': f'{member_name} joined lobby {lobby_code}'}), 200
    else:
        return jsonify({'message': 'Invalid lobby code or lobby is full'}), 400

@app.route('/leave_lobby', methods=['POST'])
def leave_lobby():
    data = request.get_json()
    lobby_id = data.get('lobby_id')
    member_name = data.get('member_name')

    if not lobby_id or not member_name:
        return jsonify({'message': 'Lobby ID and member name are required'}), 400

    member = Member(member_name)
    if server.leave_lobby(lobby_id, member):
        return jsonify({'message': f'{member_name} left lobby {lobby_id}'}), 200
    else:
        return jsonify({'message': 'Could not leave lobby'}), 400

@app.route('/get_lobby_members', methods=['GET'])
def get_lobby_members():
    lobby_id = request.args.get('lobby_id')

    if not lobby_id:
        return jsonify({'message': 'Lobby ID is required'}), 400

    try:
        members = server.get_lobby_members(int(lobby_id))
        member_names = [member.name for member in members]
        return jsonify({'members': member_names}), 200
    except ValueError:
        return jsonify({'message': 'Invalid lobby ID'}), 400

if __name__ == '__main__':
    app.run(debug=True)
    print(f"http://127.0.0.1:5000/")
