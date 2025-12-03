"""Run this model in Python

> pip install openai
"""

# Flask backend for CAIR chat app
import os
import base64
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from app_config import MONGO_URI, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from clinical_symptom_ontology import clinical_symptom_ontology

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

# Helper: Save message to MongoDB
def save_message_to_db(payload):
    db.chats.insert_one(payload)

# Helper: Get current timestamp
from datetime import datetime
def now():
    return datetime.utcnow().isoformat()

# API: Send message (handles all bandwidths)
@app.route('/api/send_message', methods=['POST'])
def send_message():
    # High bandwidth: FormData (multipart)
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        form = request.form
        files = request.files
        name = form.get('name')
        age = form.get('age')
        sex = form.get('sex')
        pain = form.get('pain')
        symptoms = form.get('symptoms')
        message = form.get('message')
        bandwidth = 'high'
        image_paths = []
        for file_key in files:
            file = files[file_key]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_paths.append(filepath)
        # Save user message
        user_payload = {
            'role': 'user',
            'name': name,
            'age': age,
            'sex': sex,
            'pain': pain,
            'symptoms': symptoms,
            'message': message,
            'images': image_paths,
            'bandwidth': bandwidth,
            'timestamp': now()
        }
        save_message_to_db(user_payload)
    else:
        # Low/Medium bandwidth: JSON
        data = request.get_json(force=True)
        name = data.get('name')
        age = data.get('age')
        sex = data.get('sex')
        pain = data.get('pain')
        symptoms = data.get('symptoms')
        message = data.get('message')
        bandwidth = data.get('bandwidth', 'low')
        user_payload = {
            'role': 'user',
            'name': name,
            'age': age,
            'sex': sex,
            'pain': pain,
            'symptoms': symptoms,
            'message': message,
            'images': [],
            'bandwidth': bandwidth,
            'timestamp': now()
        }
        save_message_to_db(user_payload)

    # Build agent input
    agent_messages = [
        {
            "role": "system",
            "content": "You are CAIR (Clinical Agent for Intelligent Response), an assistive clinical reasoning agent designed to support non-specialist healthcare workers in low-resource or rural environments. You do NOT replace a medical professional. Your job is to provide structured, safe, supportive guidance based only on the symptoms and image descriptions provided by the user."
        }
    ]
    # Get all chat history for this bandwidth
    history = list(db.chats.find({'bandwidth': bandwidth}, {'_id': 0}))
    for msg in history:
        if msg['role'] == 'user':
            agent_messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": msg.get('message', '') or msg.get('symptoms', '')}
                ]
            })
            # If images, add as image_url
            for img_path in msg.get('images', []):
                agent_messages[-1]['content'].append({
                    "type": "image_url",
                    "image_url": {"url": encode_image(img_path, "image/png")}
                })
        elif msg['role'] == 'assistant':
            agent_messages.append({
                "role": "assistant",
                "content": [
                    {"type": "text", "text": msg.get('response', msg.get('content', ''))}
                ]
            })

    # Call CAIR agent
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
    # Save CAIR response
    assistant_payload = {
        'role': 'assistant',
        'response': assistant_reply,
        'bandwidth': bandwidth,
        'timestamp': now()
    }
    save_message_to_db(assistant_payload)
    return jsonify({'response': assistant_reply})

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
        db.images.insert_one({'filename': filename, 'path': filepath, 'timestamp': now()})
        return jsonify({'status': 'ok', 'filename': filename, 'path': filepath})
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/chat_history')
def chat_history():
    bandwidth = request.args.get('bandwidth')
    history = list(db.chats.find({'bandwidth': bandwidth}, {'_id': 0}))
    return jsonify({'history': history})

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    db.chats.delete_many({})
    db.images.delete_many({})
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

