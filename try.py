# from pymongo import MongoClient
# from flask import Flask, request, render_template
# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer
# from pyttsx3 import engine
# from requests import get
# from bs4 import BeautifulSoup
# import os
# import pyttsx3
# from queue import Queue
# # from googlesearch import search
# # import requests
# from flask import jsonify
#
# app = Flask(__name__)
#
# # Initialize a queue to handle text-to-speech requests
# tts_queue = Queue()
# # Initialize the MongoDB client
# client = None
#
# # Initialize the ChatBot
# bot = ChatBot('ChatBot')
# trainer = ListTrainer(bot)
#
# # Train the chatbot with data
# for file in os.listdir('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data'):
#     chats = open('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data\\' + file, 'r').readlines()
#     chats = [chat.lower() for chat in chats]
#     trainer.train(chats)
#
# THRESHOLD_SIMILARITY = 10  # Adjust the threshold as needed
#
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)  # Index 1 usually corresponds to a female voice, but you can test to ensure
#
#
# @app.route("/")
# def hello():
#     return render_template('chat.html')
#
#
# @app.route("/ask", methods=['POST'])
# def ask():
#     global client
#
#     # Reinitialize the MongoDB client if it's closed
#     if client is None:
#         client = MongoClient('mongodb://localhost:27017/')
#
#     # Get user's message
#     message = str(request.form['messageText'])
#
#     # Get chatbot's response
#     bot_response = bot.get_response(message)
#
#     # Insert conversation into MongoDB collection
#     conversation_entry = {
#         'user_message': message,
#         'bot_response': str(bot_response)
#     }
#     try:
#         db = client['data']  # Choose or create a database
#         collection = db['chat']  # Choose or create a collection
#         collection.insert_one(conversation_entry)
#     except Exception as e:
#         print("Error inserting conversation into MongoDB:", e)
#
#     # Check chatbot's confidence
#     if bot_response.confidence > 0.1:
#         response_text = str(bot_response)
#     elif message == "bye":
#         response_text = 'Hope to see you soon'
#     else:
#         try:
#             url = "https://en.wikipedia.org/wiki/" + message
#             page = get(url).text
#             soup = BeautifulSoup(page, "html.parser")
#             p = soup.find_all("p")
#             response_text = p[1].text
#         except IndexError as error:
#             response_text = 'Sorry, I have no idea about that.'
#
#     tts_queue.put(response_text)
#
#     return jsonify({'status': 'OK', 'answer': response_text})
#
#
# def handle_tts_requests():
#     while True:
#         # Get request from the queue
#         text = tts_queue.get()
#
#         # Convert text to speech using pyttsx3
#         engine.say(text)
#         engine.runAndWait()
#
#
# # Start a separate thread to handle text-to-speech requests
# from threading import Thread
#
# tts_thread = Thread(target=handle_tts_requests)
# tts_thread.daemon = True
# tts_thread.start()
#
# if __name__ == "__main__":
#     app.run()


from pymongo import MongoClient
from flask import Flask, request, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from pyttsx3 import init, engine
from requests import get
from bs4 import BeautifulSoup
import os
import pyttsx3
from queue import Queue
from flask import jsonify
import threading

from try2 import voices

app = Flask(__name__)

# Initialize a queue to handle text-to-speech requests
tts_queue = Queue()
# Initialize the MongoDB client
client = None

# Initialize the ChatBot
bot = ChatBot('ChatBot')
trainer = ListTrainer(bot)

# Train the chatbot with data
for file in os.listdir('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data'):
    chats = open('C:\\Users\\charu\\PycharmProjects\\flaskProject1\\data\\' + file, 'r').readlines()
    chats = [chat.lower() for chat in chats]
    trainer.train(chats)

THRESHOLD_SIMILARITY = 10  # Adjust the threshold as needed


# engine = init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)  # Index 1 usually corresponds to a female voice, but you can test to ensure


@app.route("/")
def hello():
    return render_template('chat.html')


@app.route("/ask", methods=['POST'])
def ask():
    global client

    # Reinitialize the MongoDB client if it's closed
    if client is None:
        client = MongoClient('mongodb://localhost:27017/')

    # Get user's message
    message = str(request.form['messageText'])

    # Get chatbot's response
    bot_response = bot.get_response(message)

    # Insert conversation into MongoDB collection
    conversation_entry = {
        'user_message': message,
        'bot_response': str(bot_response)
    }
    try:
        db = client['data']  # Choose or create a database
        collection = db['chat']  # Choose or create a collection
        collection.insert_one(conversation_entry)
    except Exception as e:
        print("Error inserting conversation into MongoDB:", e)

    # Check chatbot's confidence
    if bot_response.confidence > 0.1:
        response_text = str(bot_response)
    elif message == "bye":
        response_text = 'Hope to see you soon'
    else:
        try:
            url = "https://en.wikipedia.org/wiki/" + message
            page = get(url).text
            soup = BeautifulSoup(page, "html.parser")
            p = soup.find_all("p")
            response_text = p[1].text
        except IndexError as error:
            response_text = 'Sorry, I have no idea about that.'

    return jsonify({'status': 'OK', 'answer': response_text})


# def handle_tts_requests():
#     while True:
#         # Get request from the queue
#         text = tts_queue.get()
#
#         # Convert text to speech using pyttsx3
#         engine.say(text)
#         engine.runAndWait()
#
#
# # Start a separate thread to handle text-to-speech requests
# tts_thread = threading.Thread(target=handle_tts_requests)
# tts_thread.daemon = True
# tts_thread.start()

def handle_tts_requests():
    while True:
        # Get request from the queue
        text = tts_queue.get()

        # Initialize the pyttsx3 engine
        engine = pyttsx3.init()

        # Get all available voices
        voices = engine.getProperty('voices')

        # Set the female voice if available
        female_voice = None
        for voice in voices:
            if "female" in voice.name.lower():
                female_voice = voice
                break

        if female_voice:
            engine.setProperty('voice', female_voice.id)

        # Convert text to speech using pyttsx3
        engine.say(text)
        engine.runAndWait()


if __name__ == "__main__":
    app.run()
