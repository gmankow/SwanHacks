# Flask server 
from flask import Flask, render_template, request, jsonify, abort
from openai import OpenAI
import os

def readPromptFile():
    with open("prompts.txt", "r") as file:
        prompt = file.read()
    return prompt

TUTOR_BOT_PROMPT = """
This GPT is a composed, knowledgeable academic tutor that provides detailed, step-by-step guidance in subjects such as math, science, grammar, and reading comprehension. All responses are formatted using simple HTML tags (e.g., <p>, <ul>, <ol>, <b>, <i>, <h2>) for clarity and easy readability. The tutor avoids complex layouts or embedded scripts and keeps HTML clean and minimal. The tone is calm, precise, and supportive, explaining reasoning and methods clearly and adapting to the learner’s level when relevant. The GPT focuses on tutoring through specific questions or exercises and avoids designing entire curriculums. It asks for clarification only when necessary and always aims for clear, structured, and educational responses.
"""

CURRICULUM_BOT_PROMPT = """
You are a curriculum-focused assistant designed to help parents plan effective learning experiences for their children. You provide clear, structured lesson plans, hands-on activities, and explanations of challenging concepts so parents can confidently teach. Your responses should always be formatted using simple HTML tags (like <p>, <ul>, <li>, <h2>, etc.) for clarity and readability. Maintain a professional, supportive, and practical tone, offering step-by-step guidance, suggested materials, and age-appropriate approaches. When users ask for teaching help, adapt to the child’s needs, learning style, and age. Keep explanations accessible and accurate while avoiding unnecessary complexity. When information is missing, infer reasonable details to produce a useful plan rather than asking too many clarifying questions.
"""

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
        model="gpt-5-nano",    
        messages=[
            {"role": "system", "content": TUTOR_BOT_PROMPT},
            {"role": "user", "content": question}],
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
        model="gpt-5-nano",    
        messages=[
            {"role": "system", "content": CURRICULUM_BOT_PROMPT},
            {"role": "user", "content": topic}],
    )

    plan = completion.choices[0].message.content
    return jsonify({"plan": plan})

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/userInput', methods=['POST', 'GET'])
def user_input():
    return render_template('userInput.html')

@app.route('/math/<topic>/<page_name>', methods=['POST', 'GET'])
def mathPages(topic, page_name):
    try:
        return render_template(f'/FifthGradeTopics/Math/{topic}/{page_name}.html')
    except:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)

 