from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit
import os
from collections import defaultdict

app = Flask(__name__)
app.secret_key = os.urandom(16)  # for sessions
socketio = SocketIO(app)

#dictionary for users in chat room
active_users = {}

messages = defaultdict(list)

@app.route("/", methods = {'GET', 'POST'})
def login():
    if request.method == 'POST':
        username = request.form.get('username')

        if username in active_users:
            return render_template('login.html', error = 'Username is taken')

        active_users[username] = request.remote_addr
        session['username'] = username
        return redirect(url_for("chat"))
    return render_template('login.html', error = None)

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username = session['username'], messages = messages)

@socketio.on('connect')
def handle_connect():
    if 'username' not in session:
        return False
    username = session['username']
    emit("chat_message", {"username": "Server", "message": f"{username} just joined!"}, broadcast=True)
    print(f"{username} connected")


@socketio.on('chat_message')
def handle_chat_message(data):
    username = session.get("username", "anon")
    msg = data.get("message", "")
    print(f"{username}: {msg}")
    emit("chat_message", {"username": username, "message": msg}, broadcast=True)
    messages[username].append(msg)

@socketio.on("disconnect")
def handle_disconnect():
    username = session.get("username")
    if username:
        del active_users[username]
        print(f"{username} disconnected")
        emit("chat_message", {"username": "Server", "message": f"{username} just left!"}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)




