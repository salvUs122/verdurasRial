import os
import firebase_admin
from firebase_admin import credentials, db

ARCHIVO_CLAVE = "credenciales.json"
URL_BASE_DATOS = "https://verduras-app-76b8a-default-rtdb.firebaseio.com/"

def conectarBaseDatos():
    if not firebase_admin._apps:
        carpetaRaiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rutaClave = os.path.join(carpetaRaiz, ARCHIVO_CLAVE)

        if not os.path.exists(rutaClave):
            raise FileNotFoundError(
                f"No se encontró '{ARCHIVO_CLAVE}' en la raíz del proyecto."
            )

        claveCredencial = credentials.Certificate(rutaClave)
        firebase_admin.initialize_app(claveCredencial, {"databaseURL": URL_BASE_DATOS})

    return db.reference("/")