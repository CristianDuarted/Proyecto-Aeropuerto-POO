import re  # Sirve para validar los datos de entrada del usuario, como nombres, correos electrónicos y números de teléfono.


# ── Utilidades de consola ──────────────────────────────────────
# Se usa para leer datos de entrada del usuario desde la consola y para mostrar mensajes de salida en la consola.
class Consola:
    def _leer_texto(self, mensaje: str) -> str:
        return input(mensaje).strip()

    def _leer_texto_no_vacio(self, mensaje: str) -> str:
        while True:
            texto = self._leer_texto(mensaje)
            if texto:
                return texto
            print("  Error, este campo no puede quedar vacío")

    def _leer_entero(self, mensaje: str) -> int:
        while True:
            try:
                valor = int(input(mensaje))
                return valor
            except ValueError:
                print("Error, ingresa un número entero válido, por favor")

    def _leer_decimal(self, mensaje: str) -> float:
        while True:
            try:
                valor = float(input(mensaje))
                return valor
            except ValueError:
                print("Error, ingresa un número decimal válido, por favor")

    def _leer_booleano(self, mensaje: str) -> bool:
        while True:
            respuesta = input(mensaje).strip().lower()
            if respuesta in ["s", "n"]:
                return respuesta == "s"
            print("Error, ingresa solo s o n, por favor")

    def _validacion(self, mensaje: str, patron: str | list[str]) -> str:
        # Permite eliminar espacios en blanco al inicio y al final de la cadena antes de realizar la validación.
        # Luego, se utiliza re.match() para verificar si cumple con la expresión regular definida en patron.
        while True:
            respuesta = self._leer_texto(mensaje)
            if isinstance(patron, str):
                if re.match(patron, respuesta):
                    return respuesta
            if isinstance(patron, list):
                if respuesta.upper() in patron:
                    return respuesta.upper()
            print("Error, ingresa el dato correctamente, por favor")

    def _leer_decimal_positivo(self, mensaje: str) -> float:
        while True:
            valor = self._leer_decimal(mensaje)
            if valor > 0:
                return valor
            print("Error, ingresa el dato correctamente, por favor")

    def _leer_prioridad(self) -> int:
        while True:
            prioridad = self._leer_entero(
                "Prioridad del vuelo (1=emergencia, 2=urgente, 3=carga, "
                "4=internacional, 5=normal): "
            )
            if 1 <= prioridad <= 5:
                return prioridad
            print("  Error, la prioridad debe estar entre 1 y 5")

    def _leer_entero_positivo(self, mensaje: str) -> int:
        while True:
            valor = self._leer_entero(mensaje)
            if valor > 0:
                return valor
            print("  Error, el valor debe ser mayor que 0")
