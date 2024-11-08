from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    
    # Start the conversation
    gather = Gather(input="speech", action="/gather_name", timeout=5)
    gather.say("Hello, this is Sky Medical Assistant. How can I help you?")
    response.append(gather)

    # If no input is received
    response.say("We didn't receive your input. Goodbye!")
    
    return Response(str(response), mimetype="text/xml")

@app.route("/gather_name", methods=["POST"])
def gather_name():
    user_input = request.form.get("SpeechResult")
    response = VoiceResponse()

    # Respond to user's input
    response.say(f"You said: {user_input}. Would you like to book an appointment for the doctor?")
    
    gather = Gather(input="speech", action="/gather_details", timeout=5)
    response.append(gather)

    return Response(str(response), mimetype="text/xml")

@app.route("/gather_details", methods=["POST"])
def gather_details():
    user_input = request.form.get("SpeechResult")
    response = VoiceResponse()

    # Confirm appointment
    response.say(f"You said: {user_input}. Please provide me your name and age.")
    
    gather = Gather(input="speech", action="/confirm_appointment", timeout=5)
    response.append(gather)

    return Response(str(response), mimetype="text/xml")

@app.route("/confirm_appointment", methods=["POST"])
def confirm_appointment():
    user_input = request.form.get("SpeechResult")
    response = VoiceResponse()

    # Confirmation message
    response.say(f"Thank you, {user_input}. Your appointment is booked between 2 to 3 PM tomorrow, 1st October.")
    response.say("Goodbye!")

    return Response(str(response), mimetype="text/xml")

if __name__ == "__main__":
    app.run(debug=True)
