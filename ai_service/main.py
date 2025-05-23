from flask import Flask, request, jsonify
from openai_utils import generate_summary

app = Flask(__name__)

@app.route('/summary', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get("text", "")
    title = data.get("title", "Untitled")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    summary = generate_summary(title, text)
    return jsonify({"summary": summary}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
