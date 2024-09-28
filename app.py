from flask import Flask, request, Blueprint, render_template
from flask_socketio import emit, SocketIO
from googletrans import Translator
from langdetect import *

translator = Translator()

def translate_message(source, dest):
    return translator.translate(text= source, dest = dest)






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
def handle_user_join(data):
    username = data["username"]
    lang = data["lang"]
    print(f"User {username} joined with preferred language {lang}!")
    users[username] = {"sid": request.sid, "lang": lang}




@socketio.on("new_message")
def handle_new_message(message):

    print(f"New message: {message}")
    sender_username = None

    # Identify the sender and their language
    for user in users:
        if users[user]["sid"] == request.sid:
            sender_username = user
            sender_lang = users[sender_username]["lang"]
            print("Sender: " + sender_username + ", Language: " + sender_lang)
            break

    # Translate the message for each user
    for user, info in users.items():
        if user == sender_username:
            # Send the original message back to the sender
            emit("chat", {"message": message, "username": sender_username, "lang": sender_lang}, room=info["sid"])
        else:
            # Translate message to the other user's language
            translated_message = translate_message(message, info["lang"]).text
            emit("chat", {"message": translated_message, "username": sender_username, "lang": info["lang"]}, room=info["sid"])


    
    
   
 


   

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'secret'
    app.register_blueprint(main)
    socketio.init_app(app, async_mode='eventlet' )

    return app


app = create_app()

socketio.run(app)
