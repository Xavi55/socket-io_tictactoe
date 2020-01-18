from flask import Flask, render_template
from flask_socketio import SocketIO, emit, rooms,join_room, leave_room

app=Flask(__name__)
app.config['SECRET_KEY']='secret1'
socketio=SocketIO(app)
###
clients={} #{<room>:{'x':<name>,'o':<name>}}


###
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('createRoom')
def handle(data):
    name=data['name']
    room=data['room']
    join_room(room)
    emit('cast',{'message':'{} created and entered {}'.format(name,room)}, room=room)

@socketio.on('joinRoom')
def handle(data):
    name=data['name']
    room=data['room']
    success=False
    second=0

    try:
        players=len(clients[room])
        if players==2:
            print('room full')
            emit('joined',{
                'message':'room {} is full'.format(room),
                'okay':0
            })
        
        else:
            join_room(room)
            clients[room]['o']=name
            second=1
            success=True

    except KeyError as e:
        join_room(room)
        clients[room]={'x':name}
        okay=True

    if success:
        emit('joined',{
            'message':'{} has joined {}'.format(name, room),
            'okay':1,
            'second':second
        }, room=room)
    print(clients)

@socketio.on('play')
def handle(data):
    room=data['room']
    move=data['move']
    player=data['player']
    emit('cast',{player:move}, room=room)

@socketio.on('check')
def handle(data):
    print(rooms())

###
if __name__ == '__main__':
    socketio.run(app, debug=True)