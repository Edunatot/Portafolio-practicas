import speech_recognition as speech
import requests
import time

sound = speech.Recognizer()

ACCESS_TOKEN = "YOUR ACCESS TOKEN FROM META DEVELOPERS"
PHONE_NUMBER_ID = "YOUR PHONE NUMBER ID FROM WHATSAPP BUSSINES"
RECIPIENT_NUMBER = "YOUR NUMBER PHONE"

com = ["yes", "no", "hi", "hello", "bye"]

def send_whatsapp(message="Alert detected"):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "from": PHONE_NUMBER_ID,
        "to": RECIPIENT_NUMBER,
        "type": "text",
        "text": {"body": mensaje} 
    }
    r = requests.post(url, headers=headers, json=payload, timeout=10)
    r.raise_for_status() 
    return r.json()

while True:
    with speech.Microphone() as audio:
        print("Listening...")
        said = sound.listen(audio)
    try:
        text = sound.recognize_google(said, language="es-ES")
        print(f"Detected: {text}")
        for comnd in com:
            if comnd in text.lower():
                print(f"You said: {comnd}")
                resp = enviar_whatsapp(f"->|WARNING: detected word '{comnd}'")
                print("Sent:", resp)
    except speech.UnknownValueError:
        print("[No recognized words]")
    except speech.RequestError as e:
        print("[Error connecting to Google]", e)

