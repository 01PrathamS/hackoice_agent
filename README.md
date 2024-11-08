# hackoice_agent
Voice Agent

# How to Run this Project 

1. Clone the repository
```
git clone <repo-url>
cd hackoice_agent
```

2. Create and activate a virtual environment(optional but recommented)
```
python -m venv venv
source venv/bin/activate
```

3. Install the required libraries 
```
pip install -r requirements.txt
```

4. Create a .env file and set up the environment variables 
```
GROQ_API_KEY=<your_groq_api_key>
TWILIO_ACCOUNT_SID=<your_twilio_account_sid>
TWILIO_AUTH_TOKEN=<your_twilio_auth_token>
TWILIO_PHONE_NUMBER=<your_twilio_phone_number>
RECIPIENT_PHONE_NUMBER=<recipient_phone_number>
NGROK_URL=<your_ngrok_url>
```

5. Running the Project 
--> Start the flask application 
```
python app.py
```
--> In another terminal, start the Twilio call script: 
```
python twilio_call.py
```

# Project Structure