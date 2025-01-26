from flask import Flask, request, jsonify, render_template
import os
import base64
from PIL import Image
import io
import openai
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Set the working API keys
os.environ['SAMBANOVA_API_KEY'] = '225c32ae-e234-421a-a625-bdb2d1dbd729'

# Constants and Configuration
SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")

def initialize_sambanova_client():
    if not SAMBANOVA_API_KEY:
        raise ValueError("SAMBANOVA_API_KEY environment variable is not set")
    openai.api_key = SAMBANOVA_API_KEY
    client = openai.OpenAI(
        api_key=SAMBANOVA_API_KEY,
        base_url="https://api.sambanova.ai/v1"
    )
    return client

def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")  # Saving as PNG
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{base64_image}"

def analyze_image(client, base64_image, model, responses):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "Analyze this medical image and provide a comprehensive diagnosis and recommendations, including potential next steps or treatments."},
                {"type": "image_url", "image_url": {"url": base64_image}}
            ]}
        ],
        temperature=0.1,
        top_p=0.1
    )
    responses.append(response.choices[0].message.content)

def generate_report(client, responses):
    combined_results = "\n".join(responses)
    
    response = client.chat.completions.create(
        model="Meta-Llama-3.3-70B-Instruct",  # Using the chosen text model
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": f"Generate a comprehensive report based on the following analysis results, including the diagnosis and recommendations:\n{combined_results}"}
            ]}
        ],
        temperature=0.1,
        top_p=0.1
    )
    final_report = response.choices[0].message.content
    
    return final_report

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    image = Image.open(file)
    base64_image = encode_image_to_base64(image)

    client = initialize_sambanova_client()
    models = [
        "Llama-3.2-11B-Vision-Instruct",
        "Llama-3.2-90B-Vision-Instruct"
    ]
    
    responses = []
    threads = []
    
    for model in models:
        thread = threading.Thread(target=analyze_image, args=(client, base64_image, model, responses))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    report = generate_report(client, responses)
    return jsonify({'report': report})

if __name__ == '__main__':
    app.run(debug=True)
