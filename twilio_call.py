import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, request
from twilio.twiml.voice_response import Gather
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

app = Flask(__name__)

def call_llm_groq(conversation_summary, query):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        prompt = (
            "You are a helpful medical assistant. Your job is to help the user book a medical appointment. "
            "Based on the previous conversation, continue the dialogue. "
            "If the user provides information, confirm it politely and ask for any missing details. "
            "Here is the conversation so far:\n"
            f"{conversation_summary}\n\n"
            "Now, please ask the user the next relevant question or respond based on the following input, please answer in less than 10 words:\n"
            f"{query}"
        )
        
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt
            }],
            model="llama3-8b-8192",
        )
        
        response = chat_completion.choices[0].message.content
        return response
    except Exception as e:
        return "Sorry, there was an issue processing your request."

conversation_summary = ""

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    global conversation_summary

    user_input = request.values.get('SpeechResult', None)

    if user_input:
        conversation_summary += f"User: {user_input}\n"
    
    llm_response = call_llm_groq(conversation_summary, user_input)

    conversation_summary += f"Assistant: {llm_response}\n"

    response = VoiceResponse()
    response.say(llm_response, voice='alice')

    gather = Gather(input='speech', action='/voice', method='POST')
    response.append(gather)

    return str(response)

def make_call():
    call = client.calls.create(
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        to=os.getenv("RECIPIENT_PHONE_NUMBER"),
        url=os.getenv("NGROK_URL") + '/voice'
    )
    print(f"Call initiated with SID: {call.sid}")

if __name__ == "__main__":
    make_call()
    app.run(debug=True, port=5000)