import os
from flask import Flask, request, jsonify
import wikipediaapi
import pytesseract
from PIL import Image

app = Flask(__name__)

# Specify a user agent to comply with Wikipedia's User-Agent policy
wiki = wikipediaapi.Wikipedia(
    'en',
    user_agent="EducationalAssistant/1.0 (https://github.com/pranshuljai1/Study-web2)"
)

@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    question = data.get("question")
    if question:
        page = wiki.page(question)
        if page.exists():
            return jsonify({"answer": page.summary[:500] + "..."})
    return jsonify({"answer": "Sorry, no answer found."})

# OCR for image-to-text
@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    image = Image.open(file.stream)
    text = pytesseract.image_to_string(image)
    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
