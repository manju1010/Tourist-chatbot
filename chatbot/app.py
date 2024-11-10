from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Model
model = "gpt-3.5-turbo"

# Define the client
client = OpenAI(api_key=os.getenv("OPEN_AI"))

# Store conversation history
conversation = [
    {
        "role": "system",
        "content": "You are a travel guide designed to provide information about landmarks in Paris. Speak concisely."
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    conversation.append({"role": "user", "content": user_message})
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=conversation,
            temperature=0.0,
            max_tokens=100
        )
        
        # Get response content
        bot_response = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": bot_response})
        
        return jsonify({"response": bot_response})
    
    except Exception as e:
        return jsonify({"response": "There was an error. Please try again.", "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
