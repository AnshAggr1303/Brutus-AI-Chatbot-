from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.llms import Ollama
from langchain.chains import ConversationChain
import re

app = Flask(__name__)
CORS(app)

# Initialize LLM with LLaMA 2 via Ollama
llm = Ollama(model="llama2")
conversation = ConversationChain(llm=llm)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the user message from the POST request
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message.strip():
            return jsonify({"response": "Please provide a message."})

        # Run the conversation
        response = conversation.run(f"You are a helpful assistant. Please provide direct responses without roleplay. User says: {user_message}")

        # Clean the response to remove annotations like *excited beep*
        clean_response = re.sub(r'\*.*?\*', '', response).strip()

        # Return the response
        return jsonify({"response": clean_response})

    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)