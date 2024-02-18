from pymongo import MongoClient
from flask import Flask, request, render_template, g
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os
from flask import jsonify
from fuzzywuzzy import fuzz

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
# def ask():
#     # # Reinitialize the MongoDB client if it's closed
#
#     if client is None:
#         g.client = MongoClient('mongodb://localhost:27017')
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
#     # Print conversation entry for debugging
#     print("Conversation Entry:", conversation_entry)
#     try:
#         db = client ['data']  # Choose or create a database
#         collection = db['chat']  # Choose or create a collection
#         print("Collection:", collection)  # Add this line to check the value of collection
#         collection.insert_one(conversation_entry)
#     except Exception as e:
#         print("Error inserting conversation into MongoDB:", e)
#         # Check chatbot's confidence
#         if bot_response.confidence > 0.1:
#             return jsonify({'status': 'OK', 'answer': str(bot_response)})
#         elif message == "bye":
#             return jsonify({'status': 'OK', 'answer': 'Hope to see you soon'})
#         else:
#             try:
#                 url = "https://en.wikipedia.org/wiki/" + message
#                 page = get(url).text
#                 soup = BeautifulSoup(page, "html.parser")
#                 p = soup.find_all("p")
#                 return jsonify({'status': 'OK', 'answer': p[1].text})
#
#             except IndexError as error:
#                 return jsonify({'status': 'OK', 'answer': 'Sorry, I have no idea about that.'})
#
#
# # Inside the "/ask" route
def ask():
    # Reinitialize the MongoDB client if it's closed
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

    # Search for similar questions in the dataset
    similar_question = find_similar_question(message, 'user_response')

    if similar_question:
        # Retrieve response for the similar question
        similar_response = get_response_for_question(similar_question)
        return jsonify({'status': 'OK', 'answer': similar_response})

    try:
        db = client['data']  # Choose or create a database
        collection = db['chat']  # Choose or create a collection
        collection.insert_one(conversation_entry)
    except Exception as e:
        print("Error inserting conversation into MongoDB:", e)
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

def find_similar_question(user_input, dataset_questions):
    highest_similarity = 0
    similar_question = None
    for question in dataset_questions:
        similarity = fuzz.partial_ratio(user_input.lower(), question.lower())
        if similarity > highest_similarity and similarity >= THRESHOLD_SIMILARITY:
            highest_similarity = similarity
            similar_question = question
    return similar_question

def get_response_for_question(question):
    # Assuming you have a MongoDB collection named 'responses' with documents containing
    # pairs of questions and responses
    db = client['data']  # Choose or create a database
    collection = db['chat']  # Choose or create a collection
    response_document = db.responses.find_one({'user_message': question})
    if response_document:
        return response_document['response']
    else:
        # If the question is not found in the database, return a default response
        return "I'm sorry, I don't have an answer to that question."


@app.teardown_request
def teardown_request(exception):
    client = getattr(g, 'client', None)
    if client is not None:
        client.close()


if __name__ == "__main__":
    app.run()
