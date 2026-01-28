import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", SCOPE)
CLIENT = gspread.authorize(CREDS)

SHEET = CLIENT.open("Registros_DB").sheet1

def guardar_lead(nombre, apellidos, telefono, direccion, notas):
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
    SHEET.append_row([fecha_hora, nombre, apellidos, telefono, direccion, notas])
    return True

def obtener_todos_registros():
    data = SHEET.get_all_records()
    return pd.DataFrame(data)

def actualizar_todo(dataframe):
    df_limpio = dataframe.fillna("")
    SHEET.clear()
    SHEET.update([df_limpio.columns.values.tolist()] + df_limpio.values.tolist())