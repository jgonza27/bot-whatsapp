## Requisitos Previos

Para levantar este proyecto necesitas:

1.  **Python 3.8** o superior instalado.
2.  Credenciales de acceso a la API de Google Sheets.

## Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone <https://github.com/jgonza27/bot-whatsapp.git>
    cd bot-whatsapp
    ```

2.  **Crear un entorno virtual:**
    ```bash
    # En Windows
    python -m venv venv
    .\venv\Scripts\activate

    # En Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### Ejecutar la aplicación

Para levantar el proyecto completo necesitas 3 terminales abiertas:

**Terminal 1 :**
```bash
streamlit run dashboard.py
```

**Terminal 2 :**
```bash
ngrok http 5000
```

**Terminal 3 :**
```bash
python main.py
```