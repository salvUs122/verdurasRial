import tkinter as tk
from tkinter import messagebox

from configuracion.configuracionBD import conectarBaseDatos
from interfaz.ventanaApp import ventanaApp
from servicios.servicioProductos import servicioProductos
from servicios.servicioAudio import servicioAudio

def iniciar():
    try:
        raizBD = conectarBaseDatos()
    except Exception as error:
        ventanaError = tk.Tk()
        ventanaError.withdraw()
        messagebox.showerror("Error de configuración", str(error))
        return

    productos = servicioProductos(raizBD)
    audio = servicioAudio()

    app = ventanaApp(productos, audio)
    app.ejecutar()

if __name__ == "__main__":
    iniciar()