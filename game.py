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

    if room in clients:
        emit('err',{'message':'{} already exists'.format(room)})
    else:
        join_room(room)
        clients[room]={'X':name}
        emit('entered',{'message':'{} created and entered {}'.format(name,room),'created':1}, room=room)
    
    print(clients)

@socketio.on('joinRoom')
def handle(data):
    name=data['name']
    room=data['room']

    if room in clients:
        if len(clients[room])==2:
            print('room full')
            emit('err',{
                'message':'room {} is full'.format(room)
            })
        
        else:
            join_room(room)
            clients[room]['O']=name
            emit('entered',{
            'message':'{} has joined {}'.format(name, room),
            'second':1
        }, room=room)
    else:
        emit('err',{
                'message':'room {} does not exist!'.format(room)
            })
    print(clients)

@socketio.on('prepGame')
def handle(data):
    room=data['room']
    emit('startGame',{'symbol':'X'} ,room=room)

@socketio.on('play')
def handle(data):
    room=data['room']
    move=data['move']
    symbol=data['symbol']
    emit('cast',{'symbol':symbol,'move':move}, room=room)

@socketio.on('changeTurn')
def handle(data):
    room=data['room']
    if 'start' in data:
        print('Start Game')
        emit('newTurn',{'symbol':'X'},room=room)
    else:
        symbol=''
        if data['symbol']=='X':
            symbol='O'
        else:
            symbol='X'
        emit('newTurn',{'symbol':symbol},room=room)


@socketio.on('check')
def handle(data):
    print(rooms())

###
if __name__ == '__main__':
    socketio.run(app, debug=True)