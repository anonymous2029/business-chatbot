from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# Set your OpenAI API Key here
openai.api_key = "your_openai_api_key"

# Define chatbot function
def chatbot_response(user_input, intent):
    if intent == "customer_support":
        prompt = f"Act as a customer support agent. Help the customer with: {user_input}"
    elif intent == "sales":
        prompt = f"Act as a sales representative. Provide sales information about: {user_input}"
    elif intent == "booking":
        prompt = f"Act as a booking assistant. Help with booking requests for: {user_input}"
    else:
        prompt = f"General chatbot response for: {user_input}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    intent = data.get("intent", "general")

    if not user_input:
        return jsonify({"error": "No input received"}), 400

    response = chatbot_response(user_input, intent)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
