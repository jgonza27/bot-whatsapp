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

## ▶Cómo levantar el proyecto

Una vez clonado el repositorio y con las dependencias instaladas, sigue estos comandos para iniciar la aplicación:


### 1. Ejecutar la aplicación
Una vez activo el entorno, lanza el siguiente comando:

```bash
streamlit run main.py
