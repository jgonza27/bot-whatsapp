from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os
import google_sheets as db 
import streamlit as st

app = Flask(__name__)

try:
    clave_groq = st.secrets["GROQ_API_KEY"]
except Exception as e:
    clave_groq = "ERROR_CLAVE"

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=clave_groq
)

conversation_history = {}

SYSTEM_PROMPT = """
Eres un asistente amable de una empresa. Tu objetivo es captar leads.
Debes conseguir estos datos del usuario uno a uno:
1. Nombre completo
2. Dirección
3. Confirmación de interés.
Si tienes todos los datos, responde con un JSON estricto: {"ACTION": "SAVE", "nombre": "...", "direccion": "...", "notas": "..."}
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
            temperature=0.7
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        return str(MessagingResponse().message(f"Error interno: {e}"))

    resp_twilio = MessagingResponse()
    
    if '"ACTION": "SAVE"' in bot_reply:
        try:
            db.guardar_lead("Usuario WhatsApp", "", sender_id, "Direccion capturada", incoming_msg)
            msg = resp_twilio.message("Gracias. Hemos guardado tus datos correctamente.")
            if sender_id in conversation_history:
                del conversation_history[sender_id]
        except Exception as e:
            msg = resp_twilio.message("Error al guardar datos.")
    else:
        conversation_history[sender_id].append({"role": "assistant", "content": bot_reply})
        msg = resp_twilio.message(bot_reply)

    return str(resp_twilio)

if __name__ == "__main__":
    app.run(debug=True, port=5000)