## Requisitos Previos

Para levantar este proyecto necesitas:

1.  **Python 3.8** o superior instalado.
2.  Credenciales de acceso a la API de Google Sheets.

## Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DE_TU_REPOSITORIO>
    cd nombre-de-la-carpeta
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

## Configuración

Este proyecto utiliza **Streamlit Secrets** para la conexión segura.

1.  Crea una carpeta llamada `.streamlit` en la raíz del proyecto.
2.  Dentro, crea un archivo llamado `secrets.toml`.
3.  Pega tus credenciales de Google en el siguiente formato:

```toml
[gcp_service_account]
type = "service_account"
project_id = "tu-project-id"
private_key_id = "tu-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n..."
client_email = "tu-email@tu-proyecto.iam.gserviceaccount.com"
client_id = "tu-client-id"
auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"
token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
auth_provider_x509_cert_url = "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)"
client_x509_cert_url = "[https://www.googleapis.com/robot/v1/metadata/x509/](https://www.googleapis.com/robot/v1/metadata/x509/)..."