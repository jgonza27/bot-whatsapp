import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", SCOPE)
CLIENT = gspread.authorize(CREDS)


SHEET = CLIENT.open("Registros_DB").sheet1

def guardar_lead(nombre, telefono, direccion, notas):

    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    SHEET.append_row([fecha_hora, nombre, telefono, direccion, notas])
    return True

def obtener_todos_registros():

    data = SHEET.get_all_records()
    return pd.DataFrame(data)

def actualizar_todo(dataframe):

    SHEET.clear()
    SHEET.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())