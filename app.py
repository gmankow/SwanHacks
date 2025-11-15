# Flask server 
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

def readPromptFile():
    with open("prompts.txt", "r") as file:
        prompt = file.read()
    return prompt

# create Flask app and run
app = Flask(__name__)

client = OpenAI()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    completion = client.chat.completions.create(
        model="gpt-5-nano",    
        messages=[
            {"role": "system", "content": readPromptFile()},
            {"role": "user", "content": user_message}
            ],
    )

    reply = completion.choices[0].message.content
    return jsonify({"reply": reply})

@app.route('/tutor', methods=["POST"])
def tutor():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    completion = client.chat.completions.create(
        model="gpt-InsertSpecificModelHere",    
        messages=[{"role": "user", "content": question}],
    )

    answer = completion.choices[0].message.content
    return jsonify({"answer": answer})

@app.route('/lesson_plan', methods=["POST"])
def lesson_plan():
    data = request.get_json()
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    completion = client.chat.completions.create(
        model="gpt-InsertSpecificModelHere",    
        messages=[{"role": "user", "content": topic}],
    )

    plan = completion.choices[0].message.content
    return jsonify({"plan": plan})

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/userInput.html', methods=['POST', 'GET'])
def user_input():
    return render_template('userInput.html')

if __name__ == '__main__':
    app.run(debug=True)

 