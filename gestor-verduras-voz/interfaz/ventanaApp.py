import tkinter as tk
from tkinter import ttk, messagebox
import threading

from utilidades.convertidorTexto import convertirTextoANumero

TITULO = "Gestor de Verduras por Voz"
ANCHO = 700
ALTO = 560
INTENTOS_VALOR = 2

# Espaciado (múltiplos de 4px/8px)
ESPACIADO_MINIMO = 4
ESPACIADO_BASE = 8
ESPACIADO_DOBLE = 16
ESPACIADO_TRIPLE = 24

# Paleta de colores
COLOR_VERDE_BOSQUE = "#2C3B2E"
COLOR_CREMA_MARFIL = "#F7F3E9"
COLOR_VERDE_GRISACEO = "#6B7C6E"
COLOR_VERDE_SALVIA = "#A9BBA0"
COLOR_TERRACOTA = "#B3541E"

# Tipografía
FUENTE_TITULO = ("Cambria", 20, "bold")
FUENTE_SUBTITULO = ("Cambria", 11, "bold")
FUENTE_TEXTO = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI Semibold", 11)
FUENTE_ESTADO = ("Segoe UI", 9)


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
        self.raiz.configure(bg=COLOR_CREMA_MARFIL)

        self.configurarEstilos()
        self.construirEncabezado()
        self.construirBusqueda()
        self.construirTabla()
        self.construirBotones()
        self.construirEstado()
        self.actualizarTabla()

    def configurarEstilos(self):
        estilo = ttk.Style(self.raiz)
        estilo.theme_use("clam")

        estilo.configure(
            "Titulo.TLabel",
            background=COLOR_VERDE_BOSQUE,
            foreground=COLOR_CREMA_MARFIL,
            font=FUENTE_TITULO,
            padding=ESPACIADO_BASE,
        )
        estilo.configure(
            "Fondo.TFrame",
            background=COLOR_CREMA_MARFIL,
        )
        estilo.configure(
            "Encabezado.TFrame",
            background=COLOR_VERDE_BOSQUE,
        )
        estilo.configure(
            "Cuerpo.TLabel",
            background=COLOR_CREMA_MARFIL,
            foreground=COLOR_VERDE_BOSQUE,
            font=FUENTE_TEXTO,
        )
        estilo.configure(
            "Estado.TLabel",
            background=COLOR_CREMA_MARFIL,
            foreground=COLOR_VERDE_GRISACEO,
            font=FUENTE_ESTADO,
        )
        estilo.configure(
            "TEntry",
            fieldbackground=COLOR_CREMA_MARFIL,
            bordercolor=COLOR_VERDE_SALVIA,
            borderwidth=1,
        )
        estilo.configure(
            "TButton",
            background=COLOR_VERDE_BOSQUE,
            foreground=COLOR_CREMA_MARFIL,
            font=FUENTE_BOTON,
            borderwidth=1,
            bordercolor=COLOR_VERDE_SALVIA,
            padding=ESPACIADO_BASE,
        )
        estilo.map(
            "TButton",
            background=[("active", COLOR_VERDE_GRISACEO)],
        )
        estilo.configure(
            "Treeview",
            background=COLOR_CREMA_MARFIL,
            fieldbackground=COLOR_CREMA_MARFIL,
            foreground=COLOR_VERDE_BOSQUE,
            font=FUENTE_TEXTO,
            bordercolor=COLOR_VERDE_SALVIA,
            borderwidth=1,
            rowheight=26,
        )
        estilo.configure(
            "Treeview.Heading",
            background=COLOR_VERDE_SALVIA,
            foreground=COLOR_VERDE_BOSQUE,
            font=FUENTE_SUBTITULO,
        )
        estilo.map(
            "Treeview",
            background=[("selected", COLOR_VERDE_SALVIA)],
            foreground=[("selected", COLOR_VERDE_BOSQUE)],
        )

    def construirEncabezado(self):
        marco = ttk.Frame(self.raiz, style="Encabezado.TFrame")
        marco.grid(row=0, column=0, sticky="ew")
        self.raiz.columnconfigure(0, weight=1)

        etiqueta = ttk.Label(marco, text=TITULO, style="Titulo.TLabel")
        etiqueta.pack(fill="x")

    def construirBusqueda(self):
        marco = ttk.Frame(self.raiz, style="Fondo.TFrame", padding=ESPACIADO_DOBLE)
        marco.grid(row=1, column=0, sticky="ew")

        ttk.Label(marco, text="Buscar:", style="Cuerpo.TLabel").grid(
            row=0, column=0, padx=(0, ESPACIADO_BASE)
        )

        self.textoBusqueda = tk.StringVar()
        self.textoBusqueda.trace_add("write", lambda *_: self.filtrarTabla())
        entrada = ttk.Entry(marco, textvariable=self.textoBusqueda, width=30, font=FUENTE_TEXTO)
        entrada.grid(row=0, column=1)

    def construirTabla(self):
        marco = ttk.Frame(self.raiz, style="Fondo.TFrame", padding=(ESPACIADO_DOBLE, 0))
        marco.grid(row=2, column=0, sticky="nsew")

        columnas = ("nombre", "valor", "posicion")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=10)
        self.tabla.heading("nombre", text="Verdura")
        self.tabla.heading("valor", text="Puntaje")
        self.tabla.heading("posicion", text="Posición")

        self.tabla.column("nombre", width=340, anchor="w")
        self.tabla.column("valor", width=120, anchor="center")
        self.tabla.column("posicion", width=120, anchor="center")
        self.tabla.grid(row=0, column=0, sticky="nsew")

    def construirBotones(self):
        marco = ttk.Frame(self.raiz, style="Fondo.TFrame", padding=ESPACIADO_DOBLE)
        marco.grid(row=3, column=0, sticky="ew")
        marco.columnconfigure((0, 1, 2), weight=1)

        self.botonRefrescar = ttk.Button(marco, text="Refrescar", command=self.actualizarTabla)
        self.botonRefrescar.grid(row=0, column=0, sticky="ew", padx=ESPACIADO_MINIMO)

        self.botonGrabar = ttk.Button(marco, text="Registrar por voz", command=self.iniciarGrabacion)
        self.botonGrabar.grid(row=0, column=1, sticky="ew", padx=ESPACIADO_MINIMO)

        self.botonBorrar = ttk.Button(marco, text="Eliminar", command=self.borrarSeleccion)
        self.botonBorrar.grid(row=0, column=2, sticky="ew", padx=ESPACIADO_MINIMO)

    def construirEstado(self):
        self.varEstado = tk.StringVar(value="Listo.")
        self.etiquetaEstado = ttk.Label(
            self.raiz, textvariable=self.varEstado, style="Estado.TLabel", padding=ESPACIADO_DOBLE
        )
        self.etiquetaEstado.grid(row=4, column=0, sticky="w")

    def actualizarTabla(self):
        try:
            self.listaCompleta = self.servicioProductos.obtenerProductos()
        except Exception as error:
            self.mostrarEstado(f"Error al leer la base de datos: {error}", tipo="error")
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
        self.mostrarEstado(f"{len(visibles)} de {len(self.listaCompleta)} verdura(s).", tipo="neutro")

    def iniciarGrabacion(self):
        if self.grabando:
            return
        self.grabando = True
        self.cambiarBotones("disabled")
        threading.Thread(target=self.procesoGrabacion, daemon=True).start()

    def procesoGrabacion(self):
        try:
            self.mostrarEstado("Diga el nombre de la verdura...", tipo="neutro")
            nombre = self.servicioAudio.capturarFrase().capitalize()

            valor = None
            for intento in range(1, INTENTOS_VALOR + 1):
                self.mostrarEstado(f"Nombre: {nombre}. Ahora diga el puntaje...", tipo="neutro")
                texto = self.servicioAudio.capturarFrase()
                valor = convertirTextoANumero(texto)
                if valor is not None:
                    break
                if intento < INTENTOS_VALOR:
                    self.mostrarEstado("No se entendió el puntaje, repita por favor.", tipo="error")

            if valor is None:
                self.mostrarEstado("No se pudo interpretar el puntaje.", tipo="error")
                return

            self.raiz.after(0, self.confirmarRegistro, nombre, valor)
        except Exception as error:
            self.mostrarEstado(str(error), tipo="error")
        finally:
            self.raiz.after(0, self.finalizarGrabacion)

    def confirmarRegistro(self, nombre, valor):
        confirma = messagebox.askyesno(
            "Confirmar registro", f"Verdura: {nombre}\nPuntaje: {valor}\n\n¿Guardar?"
        )
        if not confirma:
            self.mostrarEstado("Registro cancelado.", tipo="neutro")
            return
        self.servicioProductos.registrarProducto(nombre, valor)
        self.actualizarTabla()
        self.mostrarEstado(f"Guardado: {nombre} ({valor}).", tipo="exito")

    def finalizarGrabacion(self):
        self.grabando = False
        self.cambiarBotones("normal")

    def borrarSeleccion(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            self.mostrarEstado("Selecciona una fila primero.", tipo="error")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el registro seleccionado?"):
            self.servicioProductos.borrarProducto(seleccion[0])
            self.actualizarTabla()

    def cambiarBotones(self, estado):
        self.botonGrabar.configure(state=estado)
        self.botonBorrar.configure(state=estado)
        self.botonRefrescar.configure(state=estado)

    def mostrarEstado(self, mensaje, tipo="neutro"):
        colores = {
            "exito": COLOR_VERDE_BOSQUE,
            "error": COLOR_TERRACOTA,
            "neutro": COLOR_VERDE_GRISACEO,
        }
        self.raiz.after(0, self.varEstado.set, mensaje)
        self.raiz.after(0, self.etiquetaEstado.configure, {"foreground": colores.get(tipo, COLOR_VERDE_GRISACEO)})

    def ejecutar(self):
        self.raiz.mainloop()