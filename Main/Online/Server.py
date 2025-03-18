from flask import Flask, request, jsonify, render_template
from flask_bcrypt import Bcrypt
from Lobby import LobbyServer, Member
from flask_cors import CORS 
from flask_cors import cross_origin

app = Flask(__name__)
bcrypt = Bcrypt(app)
server = LobbyServer()
CORS(app, resources={r"/*": {"origins": "*"}})  #japierdole kurwa mać

@app.route('/')
def home():
    return render_template('Main/Online/index.html')

@app.route('/create_lobby', methods=['POST'])
def create_lobby():
    lobby_id, lobby_code = server.create_lobby()
    return jsonify({'lobby_id': lobby_id, 'lobby_code': lobby_code}), 201


@app.route('/set_questions', methods=['POST'])
def set_questions():
    data = request.get_json()
    questions = data.get('questions')

    if not questions:
        return jsonify({'message': 'Questions list is required'}), 400

    server.questions = questions 
    
@app.route('/get_questions', methods=['GET'])
def get_questions():
    return server.questions, 200

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    lobby_id = data.get('lobby_id')
    member_name = data.get('member_name')
    answer = data.get('answer')

    server.submit_answer(lobby_id, member_name, answer)

    if not lobby_id or not member_name or not answer:
        return jsonify({'message': 'Lobby ID, member name, and answer are required'}), 400

    if server.submit_answer(lobby_id, member_name, answer):
        return jsonify({'message': 'Answer submitted successfully'}), 200
    else:
        return jsonify({'message': 'Failed to submit answer'}), 400

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
    
@app.route('/all_members_submitted', methods=['GET'])
def all_members_submitted():
    lobby_id = request.args.get('lobby_id')

    if not lobby_id:
        return jsonify({'message': 'Lobby ID is required'}), 400

    if server.all_members_submitted(int(lobby_id)):
        return jsonify({'all_submitted': True}), 200
    else:
        return jsonify({'all_submitted': False}), 200
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
        return jsonify({'message': 'Invalid lobby code'}), 400

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    lobby_id = data.get('lobby_id')

    if not lobby_id:
        return jsonify({'message': 'Lobby ID is required'}), 400

    if server.start_game(lobby_id):
        return jsonify({'message': 'Game started successfully'}), 200
    else:
        return jsonify({'message': 'Failed to start game'}), 400

@app.route('/is_game_started', methods=['GET'])
def is_game_started():
    lobby_id = request.args.get('lobby_id')

    if not lobby_id:
        return jsonify({'message': 'Lobby ID is required'}), 400

    if server.is_game_started(lobby_id):
        print(server.is_game_started(lobby_id))
        return jsonify({'game_started': True}), 200
    else:
        return jsonify({'game_started': False}), 200

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
@app.route('/get_lobby_member_objects', methods=['GET'])
def get_lobby_member_objects():
    lobby_id = request.args.get('lobby_id')

    if not lobby_id:
        return jsonify({'message': 'Lobby ID is required'}), 400

    try:
        members = server.get_lobby_member_objects(int(lobby_id))
        return jsonify({'members': members}), 200
    except ValueError:
        return jsonify({'message': 'Invalid lobby ID'}), 400
    
    
if __name__ == '__main__':
    app.run(debug=True)
