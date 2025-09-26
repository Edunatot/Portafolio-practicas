import speech_recognition as speech
import requests
import time

sound = speech.Recognizer()

ACCESS_TOKEN = "EAAP2cTq2yEQBPqYxMSCCVadVCbqLuZCFKIt2pvgjSQdyzvQMDqlJy9cZCsWRiarYEZAa04hRr98SRjCtxyM3kiZAXilPsN2bXEE5ZBxt7Bs1N8xOPM1ClMEX2TeuV6nYYZCyncKugqFpQXg8187n1fRe87m7ECtMzL7wxTAnRptRCeLW1NcxHT3RMdGYN8pAZDZD"
PHONE_NUMBER_ID = "801386909723542"
RECIPIENT_NUMBER = "50251377332"

com = ["disparo", "matar", "hola"]

def enviar_whatsapp(mensaje="Alerta detectada"):
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
        print("Escuchando...")
        said = sound.listen(audio)
    try:
        text = sound.recognize_google(said, language="es-ES")
        print(f"Se detectó: {text}")
        for comnd in com:
            if comnd in text.lower():
                print(f"Dijiste: {comnd}")
                resp = enviar_whatsapp(f"->|ALERTA: palabra detectada '{comnd}'")
                print("Mensaje enviado:", resp)
    except speech.UnknownValueError:
        print("[No se reconocieron palabras]")
    except speech.RequestError as e:
        print("[Error al conectarse con Google]", e)
