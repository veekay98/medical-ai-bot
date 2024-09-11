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
    return send_from_directory('static', 'frontend-aug4.html')

@app.route('/ask-question', methods=['POST'])
def ask_question():
    app.logger.info("Received a request at /ask-question")
    try:
        openai.api_key = 'xxxxx'

        data = request.json
        question = data.get('question')
        context = data.get('context', {})

        app.logger.info(f"Received question: {question}")
        app.logger.info(f"Received context: {context}")

        # Validate and clean context
        required_keys = ['name', 'age', 'sex', 'race']
        for key in required_keys:
            if key not in context:
                context[key] = 'N/A'

        # Ensure only relevant medical value is included
        if 'blood_sugar' in context:
            context_str = f"Blood Sugar Level: {context.get('blood_sugar')}, Name: {context.get('name')}, Age: {context.get('age')}, Sex: {context.get('sex')}, Race: {context.get('race')}"
        elif 'vitamin_a' in context:
            context_str = f"Vitamin A: {context.get('vitamin_a')}, Name: {context.get('name')}, Age: {context.get('age')}, Sex: {context.get('sex')}, Race: {context.get('race')}"
        elif 'vitamin_b12' in context:
            context_str = f"Vitamin B12: {context.get('vitamin_b12')}, Name: {context.get('name')}, Age: {context.get('age')}, Sex: {context.get('sex')}, Race: {context.get('race')}"
        else:
            context_str = ', '.join(f"{key}: {value}" for key, value in context.items())

        messages = [
            {"role": "system", "content": "Provide a response to the specific question asked, considering the context provided following this. Incorporate the name, age, sex and race of the patient from the following context in the response. Use that context clearly in the answer. Return a conversational response in a way that resembles a doctor talking to a patient. Address the patient in first person."},
            {"role": "user", "content": f"Context: {context_str}\nQuestion: {question}"}
        ]
        completion = openai.ChatCompletion.create(model="gpt-4", messages=messages)
        response = completion.choices[0].message['content']
        app.logger.info(f"Response from OpenAI: {response}")

        return jsonify({"answer": response})

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
