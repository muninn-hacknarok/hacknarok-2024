from flask import Flask, request
from flask_socketio import SocketIO, join_room

import chat
import uuid
import logging


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
    socketio.emit('room_opened', {"room": code}, to=request.sid)


@socketio.on('join_room')
def join_room_func(json):
    print('received json: ' + str(json))
    join_room(json['room'])
    people_in_rooms[json['room']].append(json['name'])
    socketio.emit('joined_room', {"room": json['room']}, to=request.sid)
    socketio.emit('user_joined', {"name": json['name']}, to=json['room'] + "-private")

@socketio.on('send_question')
def send_question(json):
    print("question to room: " + json['room'])
    transcription = json['transcription']
    question = chat.prompt_chat(transcription)
    if question is None:
        return
    question.id = str(uuid.uuid4())
    question.room = json['room']
    questions[question.id] = question
    socketio.emit('question_generated', question.to_dict(), to=request.sid)


@socketio.on('confirm_question')
def send_question(json):
    print("question confirm room: " + json['id'])
    question = questions[json['id']]
    socketio.emit('question', question.to_dto_dict(), room=question.room)


@socketio.on('response')
def response(json):
    print("response to question : " + json['id'])
    question = questions[json['id']]
    question.responses.append((json['response'], json['name']))
    socketio.emit('new_response', {"id": json['id'], "response": json['response'], "name": json['name']}, room=question.room + "-private")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', allow_unsafe_werkzeug=True)
