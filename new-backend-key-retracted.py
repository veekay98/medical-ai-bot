import os
import logging
from flask import Flask, request, jsonify, send_from_directory
import openai

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    app.logger.info("Home route accessed")
    return send_from_directory('static', 'new-frontend.html')

@app.route('/api/get_suggestions', methods=['POST'])
def get_suggestions():
    app.logger.info("Received a request at /api/get_suggestions")
    try:
        data = request.json
        blood_sugar = data.get('blood_sugar')
        vitamin_a = data.get('vitamin_a')
        vitamin_b12 = data.get('vitamin_b12')

        openai.api_key = 'xxxxxx'

        messages = [
            {"role": "system", "content": "Provide medical suggestions based on the input data."},
            {"role": "user", "content": f"Blood sugar: {blood_sugar}, Vitamin A: {vitamin_a}, Vitamin B12: {vitamin_b12}"}
        ]
        completion = openai.ChatCompletion.create(model="gpt-4", messages=messages)
        response = completion.choices[0].message.content
        app.logger.info(f"Response from OpenAI: {response}")

        return jsonify({"suggestions": response})

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": "An error occurred"}), 500

@app.route('/api/ask_question', methods=['POST'])
def ask_question():
    app.logger.info("Received a request at /api/ask_question")
    try:
        data = request.json
        question = data.get('question')
        context = data.get('context', {})

        openai.api_key = 'xxxxx'

        # Form the prompt with specific context and question
        context_str = ', '.join(f"{key}: {value}" for key, value in context.items())
        messages = [
            {"role": "system", "content": "Provide a response to the specific question asked, considering the context provided."},
            {"role": "user", "content": f"Context: {context_str}\nQuestion: {question}"}
        ]
        completion = openai.ChatCompletion.create(model="gpt-4", messages=messages)
        response = completion.choices[0].message.content
        app.logger.info(f"Response from OpenAI: {response}")

        return jsonify({"suggestions": response})

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
