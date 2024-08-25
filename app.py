from flask import Flask, request, Blueprint, render_template
from flask_socketio import emit, SocketIO



socketio = SocketIO()
users = {}

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = request.sid

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None 
    for user in users:
        if users[user] == request.sid:
            username = user
    emit("chat", {"message": message, "username": username }, broadcast=True)

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'secret'
    app.register_blueprint(main)
    socketio.init_app(app)

    return app


app = create_app()

socketio.run(app)
