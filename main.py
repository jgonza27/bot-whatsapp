from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os
import json
import google_sheets as db 
import streamlit as st

app = Flask(__name__)

try:
    clave_groq = st.secrets["GROQ_API_KEY"]
except Exception:
    clave_groq = "ERROR_CLAVE"

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=clave_groq
)

conversation_history = {}

SYSTEM_PROMPT = """
Eres un asistente amable de una empresa. Tu objetivo es captar leads.
Debes conseguir estos datos del usuario uno a uno:
1. Nombre
2. Apellidos
3. Dirección exacta
4. Confirmación de interés.

Si tienes todos los datos, responde con un JSON estricto: 
{"ACTION": "SAVE", "nombre": "...", "apellidos": "...", "direccion": "...", "notas": "..."}

Si te falta algún dato, sigue conversando y preguntando amablemente. NO inventes datos.
"""

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    sender_id = request.values.get('From', '')

    if sender_id not in conversation_history:
        conversation_history[sender_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    conversation_history[sender_id].append({"role": "user", "content": incoming_msg})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history[sender_id],
            temperature=0.1
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        return str(MessagingResponse().message(f"Error: {e}"))

    resp_twilio = MessagingResponse()
    
    if '"ACTION": "SAVE"' in bot_reply:
        try:
            inicio = bot_reply.find('{')
            fin = bot_reply.rfind('}') + 1
            datos_json = json.loads(bot_reply[inicio:fin])
            
            db.guardar_lead(
                datos_json.get("nombre", ""), 
                datos_json.get("apellidos", ""), 
                sender_id, 
                datos_json.get("direccion", ""), 
                datos_json.get("notas", "")
            )
            
            msg = resp_twilio.message(f"Gracias {datos_json.get('nombre')}. Hemos guardado tus datos correctamente.")
            del conversation_history[sender_id]
        except Exception:
            msg = resp_twilio.message("Gracias. Hemos recibido tus datos.")
    else:
        conversation_history[sender_id].append({"role": "assistant", "content": bot_reply})
        msg = resp_twilio.message(bot_reply)

    return str(resp_twilio)

if __name__ == "__main__":
    app.run(debug=True, port=5000)