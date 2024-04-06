from flask import Flask
from flask_socketio import SocketIO, join_room

import chat

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

questions = {}

people_in_rooms = {}


def generate_random_code():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


@socketio.on('open_room')
def open_room():
    code = generate_random_code()
    print('opened room: ' + code)
    people_in_rooms[code] = []
    join_room(code)
    join_room(code + "-private")
    socketio.emit('room_opened', {"room": code})


@socketio.on('join_room')
def join_room_func(json):
    print('received json: ' + str(json))
    join_room(json['room'])
    people_in_rooms[json['room']].append(json['name'])


@socketio.on('send_question')
def send_question(json):
    print("question to room: " + json['room'])
    transcription = json['transcription']
    question = chat.prompt_chat(transcription)
    if question is None:
        return
    question.id = generate_random_code()
    question.room = json['room']
    questions[question.id] = question
    socketio.emit('question_generated', question.to_dict())


@socketio.on('confirm_question')
def send_question(json):
    print("question to room: " + json['id'])
    question = questions[json['id']]
    socketio.emit('question', question.to_dto_dict(), room=question.room)


@socketio.on('response')
def response(json):
    print("response to question : " + json['id'])
    question = questions[json['id']]
    question.responses.append((json['response'], json['name']))
    socketio.emit('new_response', {"id": json['id'], "response": json['response'], "name": json['name']}, room=question.room + "-private")


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
