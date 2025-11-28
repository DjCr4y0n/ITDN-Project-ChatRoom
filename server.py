from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)  # for sessions
socketio = SocketIO(app)

#dictionary for users in chat room
active_users = {}

@app.route("/", methods = {'GET', 'POST'})
def login():
    if request.method == 'POST':
        username = request.form.get('username')

        if username in active_users:
            return render_template('login.html', error = 'Username is taken')

        active_users[username] = request.remote_addr
        session['username'] = username
        return render_template('chat.html', error = None)
    return render_template('login.html', error = None)

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username = session['username'])

@socketio.on('connect')
def handle_connect():
    if 'username' not in session:
        return False
    username = session['username']
    print(f"{username} connected")


@socketio.on('chat_message')
def handle_chat_message(data):
    username = session.get("username", "anon")
    msg = data.get("message", "")
    print(f"{username}: {msg}")
    emit("chat_message", {"username": username, "message": msg}, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    username = session.get("username")
    if username:
        del active_users[username]
        print(f"{username} disconnected")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000) #0.0.0.0, so it listen to devices from the network



