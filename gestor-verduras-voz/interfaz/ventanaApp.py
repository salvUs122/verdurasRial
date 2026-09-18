import tkinter as tk
from tkinter import ttk, messagebox
import threading

from utilidades.convertidorTexto import convertirTextoANumero

TITULO = "Gestor de Verduras por Voz"
ANCHO = 700
ALTO = 480
PADDING = 10
INTENTOS_VALOR = 2

class ventanaApp:

    def __init__(self, servicioProductosInstancia, servicioAudioInstancia):
        self.servicioProductos = servicioProductosInstancia
        self.servicioAudio = servicioAudioInstancia
        self.grabando = False
        self.listaCompleta = []

        self.raiz = tk.Tk()
        self.raiz.title(TITULO)
        self.raiz.geometry(f"{ANCHO}x{ALTO}")
        self.raiz.resizable(False, False)

        self.construirBusqueda()
        self.construirTabla()
        self.construirBotones()
        self.construirEstado()
        self.actualizarTabla()

    def construirBusqueda(self):
        marco = ttk.Frame(self.raiz, padding=PADDING)
        marco.grid(row=0, column=0, sticky="ew")
        ttk.Label(marco, text="Buscar:").grid(row=0, column=0, padx=(0, 8))

        self.textoBusqueda = tk.StringVar()
        self.textoBusqueda.trace_add("write", lambda *_: self.filtrarTabla())
        entrada = ttk.Entry(marco, textvariable=self.textoBusqueda, width=30)
        entrada.grid(row=0, column=1)

    def construirTabla(self):
        marco = ttk.Frame(self.raiz, padding=PADDING)
        marco.grid(row=1, column=0, sticky="nsew")

        columnas = ("nombre", "valor", "posicion")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=14)
        self.tabla.heading("nombre", text="Verdura")
        self.tabla.heading("valor", text="Puntaje")
        self.tabla.heading("posicion", text="Posición")

        self.tabla.column("nombre", width=350, anchor="w")
        self.tabla.column("valor", width=120, anchor="center")
        self.tabla.column("posicion", width=120, anchor="center")
        self.tabla.grid(row=0, column=0, sticky="nsew")

    def construirBotones(self):
        marco = ttk.Frame(self.raiz, padding=(PADDING, 0))
        marco.grid(row=2, column=0, sticky="ew")
        marco.columnconfigure((0, 1, 2), weight=1)

        self.botonRefrescar = ttk.Button(marco, text="Refrescar", command=self.actualizarTabla)
        self.botonRefrescar.grid(row=0, column=0, sticky="ew", padx=6)

        self.botonGrabar = ttk.Button(marco, text="Registrar por voz", command=self.iniciarGrabacion)
        self.botonGrabar.grid(row=0, column=1, sticky="ew", padx=6)

        self.botonBorrar = ttk.Button(marco, text="Eliminar", command=self.borrarSeleccion)
        self.botonBorrar.grid(row=0, column=2, sticky="ew", padx=6)

    def construirEstado(self):
        self.varEstado = tk.StringVar(value="Listo.")
        etiqueta = ttk.Label(self.raiz, textvariable=self.varEstado, padding=PADDING)
        etiqueta.grid(row=3, column=0, sticky="w")

    def actualizarTabla(self):
        try:
            self.listaCompleta = self.servicioProductos.obtenerProductos()
        except Exception as error:
            self.mostrarEstado(f"Error al leer la base de datos: {error}")
            return
        self.filtrarTabla()

    def filtrarTabla(self):
        filtro = self.textoBusqueda.get().strip().lower()
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        visibles = [p for p in self.listaCompleta if filtro in p["nombre"].lower()]
        for posicion, producto in enumerate(visibles, start=1):
            self.tabla.insert(
                "", "end", iid=producto["clave"],
                values=(producto["nombre"], producto["valor"], posicion),
            )
        self.mostrarEstado(f"{len(visibles)} de {len(self.listaCompleta)} verdura(s).")

    def iniciarGrabacion(self):
        if self.grabando:
            return
        self.grabando = True
        self.cambiarBotones("disabled")
        threading.Thread(target=self.procesoGrabacion, daemon=True).start()

    def procesoGrabacion(self):
        try:
            self.mostrarEstado("Diga el nombre de la verdura...")
            nombre = self.servicioAudio.capturarFrase().capitalize()

            valor = None
            for intento in range(1, INTENTOS_VALOR + 1):
                self.mostrarEstado(f"Nombre: {nombre}. Ahora diga el puntaje...")
                texto = self.servicioAudio.capturarFrase()
                valor = convertirTextoANumero(texto)
                if valor is not None:
                    break
                if intento < INTENTOS_VALOR:
                    self.mostrarEstado("No se entendió el puntaje, repita por favor.")

            if valor is None:
                self.mostrarEstado("No se pudo interpretar el puntaje.")
                return

            self.raiz.after(0, self.confirmarRegistro, nombre, valor)
        except Exception as error:
            self.mostrarEstado(str(error))
        finally:
            self.raiz.after(0, self.finalizarGrabacion)

    def confirmarRegistro(self, nombre, valor):
        confirma = messagebox.askyesno(
            "Confirmar registro", f"Verdura: {nombre}\nPuntaje: {valor}\n\n¿Guardar?"
        )
        if not confirma:
            self.mostrarEstado("Registro cancelado.")
            return
        self.servicioProductos.registrarProducto(nombre, valor)
        self.actualizarTabla()
        self.mostrarEstado(f"Guardado: {nombre} ({valor}).")

    def finalizarGrabacion(self):
        self.grabando = False
        self.cambiarBotones("normal")

    def borrarSeleccion(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            self.mostrarEstado("Selecciona una fila primero.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el registro seleccionado?"):
            self.servicioProductos.borrarProducto(seleccion[0])
            self.actualizarTabla()

    def cambiarBotones(self, estado):
        self.botonGrabar.configure(state=estado)
        self.botonBorrar.configure(state=estado)
        self.botonRefrescar.configure(state=estado)

    def mostrarEstado(self, mensaje):
        self.raiz.after(0, self.varEstado.set, mensaje)

    def ejecutar(self):
        self.raiz.mainloop()