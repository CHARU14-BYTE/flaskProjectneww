from pymongo import MongoClient
from flask import Flask, request, render_template, g
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from pyttsx3 import engine
from requests import get
from bs4 import BeautifulSoup
import os

from flask import jsonify

app = Flask(__name__)

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

THRESHOLD_SIMILARITY = 10


@app.route("/")
def hello():
    return render_template('chat.html')





@app.route("/ask", methods=['POST'])
def ask():
    # # Reinitialize the MongoDB client if it's closed

    if client is None:
        g.client = MongoClient('mongodb://localhost:27017')

    # Get user's message
    message = str(request.form['messageText'])

    # Get chatbot's response
    bot_response = bot.get_response(message)

    # Insert conversation into MongoDB collection
    conversation_entry = {
        'user_message': message,
        'bot_response': str(bot_response)
    }
    # Print conversation entry for debugging
    print("Conversation Entry:", conversation_entry)
    try:
        db = client ['data']  # Choose or create a database
        collection = db['chat']  # Choose or create a collection
        print("Collection:", collection)  # Add this line to check the value of collection
        collection.insert_one(conversation_entry)
    except Exception as e:
        print("Error inserting conversation into MongoDB:", e)
        # Check chatbot's confidence
        if bot_response.confidence > 0.1:
            return jsonify({'status': 'OK', 'answer': str(bot_response)})
        elif message == "bye":
            return jsonify({'status': 'OK', 'answer': 'Hope to see you soon'})
        else:
            try:
                url = "https://en.wikipedia.org/wiki/" + message
                page = get(url).text
                soup = BeautifulSoup(page, "html.parser")
                p = soup.find_all("p")
                return jsonify({'status': 'OK', 'answer': p[1].text})

            except IndexError as error:
                return jsonify({'status': 'OK', 'answer': 'Sorry, I have no idea about that.'})


# Inside the "/ask" route


@app.teardown_request
def teardown_request(exception):
    client = getattr(g, 'client', None)
    if client is not None:
        client.close()


if __name__ == "__main__":
    app.run()

    # if bot_response.confidence > 0.1:
    #     response_text = str(bot_response)
    # elif message == "bye":
    #     response_text = 'Hope to see you soon'
    # else:
    #     # Fallback mechanism: Search the web
    #     try:
    #         search_results = search_web(message)
    #         if search_results:
    #             response_text = "Here is what I found on the web:\n\n"
    #             for result in search_results:
    #                 response_text += f"Title: {result['title']}\n"
    #                 response_text += f"URL: {result['url']}\n"
    #                 response_text += f"Snippet: {result['snippet']}\n\n"
    #         else:
    #             response_text = "I couldn't find relevant information on the web."
    #     except Exception as e:
    #         print("Error searching the web:", e)
    #         response_text = 'Sorry, I couldn'
    #
    # # Convert text to speech using pyttsx3
    # engine.say(response_text)
    # engine.runAndWait()
    #
    # return jsonify({'status': 'OK', 'answer': response_text})

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
#     if bot_response.confidence > 0.1:
#         response_text = str(bot_response)
#     elif message == "bye":
#         response_text = 'Hope to see you soon'
#     else:
#         # Fallback mechanism: Search the web
#         try:
#             search_results = search_web(message)
#             if search_results:
#                 response_text = "Here is what I found on the web:\n\n"
#                 for result in search_results:
#                     response_text += f"Title: {result['title']}\n"
#                     response_text += f"URL: {result['url']}\n"
#                     response_text += f"Snippet: {result['snippet']}\n\n"
#             else:
#                 response_text = "I couldn't find relevant information on the web."
#         except Exception as e:
#             print("Error searching the web:", e)
#             response_text = 'Sorry, I couldn'
#
#
#         # Convert text to speech using pyttsx3 and save as MP3
#
#     return jsonify({'status': 'OK', 'answer': response_text})


# if __name__ == "__main__":
#     app.run()
