"""Run this model in Python

> pip install openai
"""

# Flask backend for CAIR chat app
import os
import base64
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from app_config import MONGO_URI, UPLOAD_FOLDER, ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.get_database()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image(path, mime_type):
    with open(path, "rb") as image:
        encoded = base64.b64encode(image.read())
    return f"data:{mime_type};base64,{encoded.decode()}"

# --- Flask routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat/<bandwidth>')
def chat_bandwidth(bandwidth):
    if bandwidth == 'low':
        return render_template('chat_low.html')
    elif bandwidth == 'medium':
        return render_template('chat_medium.html')
    elif bandwidth == 'high':
        return render_template('chat_high.html')
    else:
        return "Invalid bandwidth", 400

# --- API endpoints ---
@app.route('/api/user_info', methods=['POST'])
def save_user_info():
    data = request.json
    db.users.insert_one(data)
    return jsonify({'status': 'ok'})

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    bandwidth = data.get('bandwidth')
    # Save user message
    db.chats.insert_one({'role': 'user', 'content': message, 'bandwidth': bandwidth})
    # Build messages for agent
    history = list(db.chats.find({'bandwidth': bandwidth}, {'_id': 0, 'role': 1, 'content': 1}))
    agent_messages = [
        {
            "role": "system",
            "content": "You are CAIR (Clinical Agent for Intelligent Response), an assistive clinical reasoning agent designed to support non-specialist healthcare workers in low-resource or rural environments. You do NOT replace a medical professional. Your job is to provide structured, safe, supportive guidance based only on the symptoms and image descriptions provided by the user."
        }
    ]
    for msg in history:
        agent_messages.append({
            "role": msg['role'],
            "content": [
                {
                    "type": "text",
                    "text": msg['content']
                }
            ]
        })
    # Call agent (replace hardcoded prompt with user input)
    import openai
    client = openai.OpenAI(
        base_url = "https://models.github.ai/inference",
        api_key = os.environ.get("GITHUB_TOKEN", ""),
        default_query = {"api-version": "2024-08-01-preview"},
    )
    response = client.chat.completions.create(
        messages = agent_messages,
        model = "openai/gpt-4.1",
        response_format = {"type": "text"},
        temperature = 1,
        top_p = 1,
    )
    assistant_reply = response.choices[0].message.content if response.choices else "No response."
    db.chats.insert_one({'role': 'assistant', 'content': assistant_reply, 'bandwidth': bandwidth})
    return jsonify({'response': assistant_reply})

@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        db.images.insert_one({'filename': filename, 'path': filepath})
        return jsonify({'status': 'ok', 'filename': filename})
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/chat_history')
def chat_history():
    bandwidth = request.args.get('bandwidth')
    history = list(db.chats.find({'bandwidth': bandwidth}, {'_id': 0, 'role': 1, 'content': 1}))
    return jsonify({'history': history})

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    db.chats.delete_many({})
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

