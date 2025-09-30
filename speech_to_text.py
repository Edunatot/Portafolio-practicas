import speech_recognition as speech
import requests
import time

sound = speech.Recognizer()

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_FROM_META_DEVELOPERS"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID_FROM_WHATSAPP_BUSINESS"
RECIPIENT_NUMBER = "YOUR_PHONE_NUMBER"  # Incluye el código de país, ej: 502XXXXXXXX

# Palabras clave a detectar
com = ["yes", "no", "hi", "hello", "bye"]

def send_whatsapp(message="Alert detected"):
    """
    Envía un mensaje de texto libre por WhatsApp usando Cloud API.
    """
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_NUMBER,
        "type": "text",
        "text": {"body": message}
    }
    r = requests.post(url, headers=headers, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()

while True:
    with speech.Microphone() as audio:
        print("Listening...")
        said = sound.listen(audio)

    try:
        text = sound.recognize_google(said, language="en-US")
        print(f"Detected: {text}")

        for comnd in com:
            if comnd in text.lower():
                print(f"You said: {comnd}")
                resp = send_whatsapp(f"WARNING: detected word '{comnd}'")
                print("Message sent:", resp)
                break  # evita enviar más de un mensaje por cada frase

    except speech.UnknownValueError:
        print("[No recognized words]")
    except speech.RequestError as e:
        print("[Error connecting to Google]", e)

    time.sleep(0.5)


