import os
import openai
from flask import Flask, request, Response, redirect, render_template, url_for

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

        # Read the contents of the prompt.txt file
        with open("prompt.txt", "r") as f:
            prompt = f.read()

        # Generate a response from the chatbot
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )
        chatbot_response = response.choices[0].text
        conversation.append({"chatbot": chatbot_response})

    return render_template("index.html", conversation=conversation)


@app.route("/sms", methods=["POST"])
def sms():
    # Get the message body from the request
    body = request.form["Body"]

    # Read the prompt from the prompt.txt file
    with open("prompt.txt", "r") as f:
        prompt = f.read()

    # Generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\n{body}",
        temperature=0.,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    chatbot_response = response.choices[0].text



    # Create a TwiML response
    twiml_response = f"<Response><Message>{chatbot_response}</Message></Response>"

    return Response(twiml_response, mimetype="text/xml")



