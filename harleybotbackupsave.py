import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

conversation = []

@app.route("/", methods=("GET", "POST"))
def index():
    global conversation

    # Handle form submission
    if request.method == "POST":
        user_input = request.form["input"]
        conversation.append({"user": user_input})

        # Generate a response from the chatbot
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Harley helpline! How can I smash your problems into itty bitty pieces?\n{user_input}",
            temperature=0.6,
        )
        chatbot_response = response.choices[0].text
        conversation.append({"chatbot": chatbot_response})

    return render_template("index.html", conversation=conversation)


