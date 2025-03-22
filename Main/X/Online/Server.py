from flask import Flask, request, jsonify, render_template
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from Lobby import LobbyServer, Member

app = Flask(__name__)
bcrypt = Bcrypt(app)
server = LobbyServer()
CORS(app, resources={r"/*": {"origins": "*"}})

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
    return jsonify({'message': 'Questions set successfully'}), 200

@app.route('/get_questions', methods=['GET'])
def get_questions():
    return jsonify(server.questions), 200

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    lobby_id = data.get('lobby_id')
    member_name = data.get('member_name')
    answer = data.get('answer')

    if not all([lobby_id, member_name, answer]):
        return jsonify({'message': 'Lobby ID, member name, and answer are required'}), 400

    success = server.submit_answer(lobby_id, member_name, answer)
    return jsonify({'message': 'Answer submitted successfully' if success else 'Failed to submit answer'}), 200 if success else 400

@app.route('/get_lobby_id_from_code', methods=['GET'])
def get_lobby_id_from_code():
    lobby_code = request.args.get('lobby_code')
    
    if not lobby_code:
        return jsonify({'message': 'Lobby code is required'}), 400
    
    lobby_id = server.get_lobby_id_from_code(lobby_code)
    return jsonify({'lobby_id': lobby_id}) if lobby_id is not None else jsonify({'message': 'Invalid lobby code'}), 400

@app.route('/all_members_submitted', methods=['GET'])
def all_members_submitted():
    lobby_id = request.args.get('lobby_id')
    
    if not lobby_id:
        return jsonify({'message': 'Lobby ID is required'}), 400
    
    return jsonify({'all_submitted': server.all_members_submitted(lobby_id)}), 200

@app.route('/join_lobby', methods=['POST'])
def join_lobby():
    data = request.get_json()
    lobby_code = data.get('lobby_code')
    member_name = data.get('member_name')

    if not all([lobby_code, member_name]):
        return jsonify({'message': 'Lobby code and member name are required'}), 400
    
    success = server.join_lobby_with_code(lobby_code, member_name)
    return jsonify({'message': f'{member_name} joined lobby {lobby_code}' if success else 'Invalid lobby code'}), 200 if success else 400

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    lobby_id = data.get('lobby_id')

    if not lobby_id:
        return jsonify({'message': 'Lobby ID is required'}), 400
    
    success = server.start_game(lobby_id)
    return jsonify({'message': 'Game started successfully' if success else 'Failed to start game'}), 200 if success else 400

@app.route('/is_game_started', methods=['GET'])
def is_game_started():
    lobby_id = request.args.get('lobby_id')

    if not lobby_id:
        return jsonify({'message': 'Lobby ID is required'}), 400
    
    return jsonify({'game_started': server.is_game_started(lobby_id)}), 200

@app.route('/leave_lobby', methods=['POST'])
def leave_lobby():
    data = request.get_json()
    lobby_id = data.get('lobby_id')
    member_name = data.get('member_name')

    if not all([lobby_id, member_name]):
        return jsonify({'message': 'Lobby ID and member name are required'}), 400
    
    success = server.leave_lobby(lobby_id, member_name)
    return jsonify({'message': f'{member_name} left lobby {lobby_id}' if success else 'Could not leave lobby'}), 200 if success else 400

@app.route('/get_lobby_members', methods=['GET'])
def get_lobby_members():
    lobby_id = request.args.get('lobby_id')

    if not lobby_id:
        return jsonify({'message': 'Lobby ID is required'}), 400
    
    try:
        members = server.get_lobby_members(int(lobby_id))
        return jsonify({'members': members}), 200
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

@app.route('/set_round', methods=['GET'])
def set_round():
    lobby_id = request.args.get('lobby_id')
    
    if not lobby_id:
        return jsonify({'message': 'Lobby ID is required'}), 400
    
    success = server.set_round(lobby_id)
    return jsonify({'message': 'Round was set' if success else 'Invalid lobby ID'}), 200 if success else 400

if __name__ == '__main__':
    app.run(debug=True)
