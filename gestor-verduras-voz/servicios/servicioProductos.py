NODO_PRODUCTOS = "verduras"
CAMPO_NOMBRE = "nombre"
CAMPO_VALOR = "puntaje"

class servicioProductos:

    def __init__(self, raizBD):
        self.referencia = raizBD.child(NODO_PRODUCTOS)

    def registrarProducto(self, nombre, valor):
        nuevoRegistro = {
            CAMPO_NOMBRE: nombre.strip(),
            CAMPO_VALOR: int(valor),
        }
        creado = self.referencia.push(nuevoRegistro)
        return creado.key

    def obtenerProductos(self):
        datos = self.referencia.get()
        if not datos:
            return []

        lista = []
        for clave, registro in datos.items():
            if not isinstance(registro, dict):
                continue
            lista.append({
                "clave": clave,
                "nombre": registro.get(CAMPO_NOMBRE, ""),
                "valor": int(registro.get(CAMPO_VALOR, 0)),
            })

        lista.sort(key=lambda p: p["valor"])
        return lista

    def borrarProducto(self, clave):
        self.referencia.child(clave).delete()