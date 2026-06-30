"""Este programa simula un sistema de control de pasajeros en un aeropuerto.
Permite registrar información de pasajeros, validar sus documentos y equipaje
y generar un reporte final indicando los pasajeros aprobados y rechazados."""

import re  # Sirve para validar los datos de entrada del usuario, como nombres, correos electrónicos y números de teléfono.


# Se usa para leer datos de entrada del usuario desde la consola y para mostrar mensajes de salida en la consola.
class Consola:
    def leer_texto(self, mensaje: str) -> str:
        return input(mensaje)

    def leer_entero(self, mensaje: str) -> int:
        while True:
            try:
                valor = int(input(mensaje))
                return valor
            except ValueError:
                print("Error, ingresa el digito en entero por favor")

    def leer_decimal(self, mensaje: str) -> float:
        while True:
            try:
                valor = float(input(mensaje))
                return valor
            except ValueError:
                print("Error, ingresa el digito en entero o decimal por favor")

    def leer_booleano(self, mensaje: str) -> bool:
        while True:
            respuesta = input(mensaje).strip().lower()
            if respuesta in ["s", "n"]:
                return respuesta == "s"
            print("Error, ingresa solo s o n por favor")


# Esta clase representa a un pasajero y almacena su información personal, como nombre, edad, nacionalidad, tipo de sangre, teléfono, correo electrónico y destino.
class Pasajero:
    def __init__(
        self,
        nombre: str,
        edad: int,
        nacionalidad: str,
        tipo_sangre: str,
        telefono: str,
        correo: str,
        destino: str,
    ) -> None:

        self.nombre = nombre
        self.edad = edad
        self.nacionalidad = nacionalidad
        self.tipo_sangre = tipo_sangre
        self.telefono = telefono
        self.correo = correo
        self.destino = destino


# Esta clase representa los documentos de un pasajero, incluyendo el número de pasaporte, la vigencia del pasaporte y la visa, si se ha realizado el check-in y si el boleto es válido.
class Documento:
    def __init__(
        self,
        numero_pasaporte: str,
        pasaporte_vigente: bool,
        tiene_visa: bool,
        visa_vigente: bool,
        check_in_realizado: bool,
        boleto_valido: bool,
    ) -> None:

        self.numero_pasaporte = numero_pasaporte
        self.pasaporte_vigente = pasaporte_vigente
        self.tiene_visa = tiene_visa
        self.visa_vigente = visa_vigente
        self.check_in_realizado = check_in_realizado
        self.boleto_valido = boleto_valido


# Esta clase representa el equipaje de un pasajero, incluyendo la cantidad de maletas, el peso total, las dimensiones (largo, ancho y alto), entre otros.
class Equipaje:
    def __init__(
        self,
        cantidad_maletas: int,
        peso_total: float,
        largo: float,
        ancho: float,
        alto: float,
        elementos_peligrosos: bool,
        material_inflamable: bool,
        armas: bool,
    ) -> None:

        self.cantidad_maletas = cantidad_maletas
        self.peso_total = peso_total
        self.largo = largo
        self.ancho = ancho
        self.alto = alto
        self.elementos_peligrosos = elementos_peligrosos
        self.material_inflamable = material_inflamable
        self.armas = armas

        self.cargo_adicional = 0.0
        self.en_bodega = False


# Esta clase se encarga de validar la información de un pasajero, sus documentos y su equipaje.
# Si el pasajero es aprobado, también calcula los cargos adicionales por exceso de equipaje o dimensiones fuera de los límites permitidos.
class ValidadorPasajero:
    def validar_pasajero(
        self, pasajero: Pasajero, documento: Documento, equipaje: Equipaje
    ) -> tuple[bool, list[str]]:

        motivos_rechazo = []
        motivos_aprobado = []

        if pasajero.edad < 18:
            motivos_rechazo.append("Menor de edad")

        if not documento.pasaporte_vigente:
            motivos_rechazo.append("Pasaporte vencido")

        paises_con_visa = ["canada", "estados unidos", "australia", "reino unido"]

        if pasajero.destino.lower() in paises_con_visa:
            if not documento.tiene_visa:
                motivos_rechazo.append("El destino requiere visa")

            if not documento.visa_vigente:
                motivos_rechazo.append("Visa vencida")

        if not documento.check_in_realizado:
            motivos_rechazo.append("No realizó check-in")

        if not documento.boleto_valido:
            motivos_rechazo.append("Boleto inválido")

        if equipaje.armas:
            motivos_rechazo.append("Transporta armas")

        if equipaje.material_inflamable:
            motivos_rechazo.append("Material inflamable")

        if equipaje.elementos_peligrosos:
            motivos_rechazo.append("Elementos peligrosos")

        self.validar_equipaje(equipaje)

        motivos_aprobado.append("Aprobado")

        if motivos_rechazo:
            return False, motivos_rechazo

        return True, motivos_aprobado

    def validar_equipaje(self, equipaje: Equipaje) -> None:

        if equipaje.cantidad_maletas < 1:
            return

        if equipaje.cantidad_maletas > 3.0:
            exceso = equipaje.cantidad_maletas - 3.0

            equipaje.cargo_adicional += exceso * 50000.0
            equipaje.en_bodega = True

        if equipaje.peso_total > 23.0:
            exceso = equipaje.peso_total - 23.0

            equipaje.cargo_adicional += exceso * 10000.0
            equipaje.en_bodega = True

        if equipaje.largo > 55 or equipaje.ancho > 40 or equipaje.alto > 25:
            equipaje.cargo_adicional += 50000.0
            equipaje.en_bodega = True


# Esta clase representa el sistema de control de pasajeros en un aeropuerto. Permite registrar pasajeros, validar sus documentos y equipaje.
# Generando un reporte final indicando los pasajeros aprobados y rechazados.
class SistemaAeropuerto:
    def __init__(self) -> None:

        self.aprobados: list[
            tuple[Pasajero, Equipaje]
        ] = []  # Lista de pasajeros aprobados
        self.rechazados: list[
            tuple[Pasajero, str]
        ] = []  # Lista de pasajeros rechazados

        self.consola = Consola()
        self.validador = ValidadorPasajero()

    def registrar_pasajero(self) -> None:

        cantidad = self.consola.leer_entero("¿Cuántos pasajeros desea registrar?: ")
        # Sirve para registrar la información de los pasajeros, dependiendo de la cantidad que el usuario ingrese
        # Se ejecutará un ciclo que solicitará los datos de cada pasajero.
        for _ in range(cantidad):
            print("\n" + "=" * 60)
            print(
                f"REGISTRO DE PASAJERO N° {len(self.aprobados) + len(self.rechazados) + 1}"
            )
            print("=" * 60)

            # Validar nombre (solo letras, espacios, apóstrofes y guiones)
            Nombre_regla = r"^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s'-]+$"
            nombre = self.consola.leer_texto("Nombre: ")
            while True:
                if re.match(Nombre_regla, nombre.strip()):
                    break
                else:
                    print(
                        "Error, ingresa solo letras (con espacios si llega ser el caso), por favor"
                    )
                    nombre = self.consola.leer_texto("Nombre: ")

            edad = self.consola.leer_entero("Edad: ")

            # Validar nacionalidad (solo letras y espacios)
            reglas = r"^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$"
            nacionalidad = self.consola.leer_texto("Nacionalidad: ")
            while True:
                # Permite eliminar espacios en blanco al inicio y al final de la cadena antes de realizar la validación.
                # Luego, se utiliza re.match() para verificar si la nacionalidad ingresada cumple con la expresión regular definida en reglas.
                if re.match(reglas, nacionalidad.strip()):
                    break
                else:
                    print(
                        "Error, ingresa solo letras (con espacios si llega ser el caso), por favor"
                    )
                    nacionalidad = self.consola.leer_texto("Nacionalidad: ")

            # Validar tipo de sangre (solo opciones válidas)
            Tipo_sangre_regla = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
            tipo_sangre = self.consola.leer_texto("Tipo de sangre: ")
            while True:
                if tipo_sangre in Tipo_sangre_regla:
                    break
                else:
                    print("Error, ingresa el tipo de sangre correcto, por favor")
                    tipo_sangre = self.consola.leer_texto("Tipo de sangre: ")

            # Validar teléfono (solo números y espacios, puede iniciar con +)
            telefono_regla = r"^\+?[0-9\s]+$"
            telefono = self.consola.leer_texto("Teléfono: ")
            while True:
                # Permite eliminar espacios en blanco al inicio y al final de la cadena antes de realizar la validación.
                # Luego, se utiliza re.match() para verificar si el teléfono ingresado cumple con la expresión regular definida en telefono_regla.
                if re.match(telefono_regla, telefono.strip()):
                    break
                else:
                    print("Error, ingresa nuevamente su número de teléfono, por favor")
                    telefono = self.consola.leer_texto("Teléfono: ")

            correo = self.consola.leer_texto("Correo: ")
            # Validar correo (solo direcciones de correo válidas)
            correo_regla = [
                "unal.edu.co",
                "gmail.com",
                "hotmail.com",
                "icloud.com",
                "outlook.com",
                "yahoo.com",
                "protonmail.com",
            ]
            # Verifica si el correo ingresado cumple con las condiciones de validación.
            while True:
                correo_limpio = correo.strip()  # Se eliminan los espacios en blanco al inicio y al final del correo ingresado.
                count_arroba = correo_limpio.count(
                    "@"
                )  # Se cuenta la cantidad de veces que aparece el símbolo "@" en el correo ingresado por el usuario.

                # No cumple si el correo está vacío, contiene espacios o tiene más de un símbolo "@".
                if (
                    (correo_limpio == "")
                    or (" " in correo_limpio)
                    or (count_arroba != 1)
                ):
                    print("Error, digite correctamente su correo, por favor")
                    correo = self.consola.leer_texto("Correo: ")
                    continue

                # Se divide el correo en dos partes: la parte del usuario y el dominio, utilizando el símbolo "@" como separador.
                parte_usuario, dominio = correo_limpio.split("@", 1)
                # No cumple si la parte del usuario está vacía.
                if parte_usuario == "":
                    print("Error, digite correctamente su correo, por favor")
                    correo = self.consola.leer_texto("Correo: ")
                    continue
                # No cumple si el dominio no está en la lista de dominios permitidos.
                if dominio not in correo_regla:
                    print("Error, digite correctamente su correo, por favor")
                    correo = self.consola.leer_texto("Correo: ")
                else:
                    correo = correo_limpio
                    break

            destino = self.consola.leer_texto("Destino: ")
            while True:
                if re.match(reglas, destino.strip()):
                    break
                print(
                    "Error, ingresa solo letras (con espacios si llega ser el caso), por favor"
                )
                destino = self.consola.leer_texto("Destino: ")

            print("\nDOCUMENTOS")
            # Validar pasaporte (solo letras y números)
            pasaporte_reglas = r"^[a-zA-Z0-9]+$"
            numero_pasaporte = self.consola.leer_texto("Pasaporte: ")
            while True:
                if re.match(pasaporte_reglas, numero_pasaporte.strip()):
                    break
                else:
                    print("Error, Solo se acepta letras/numeros, por favor")
                    numero_pasaporte = self.consola.leer_texto("Pasaporte: ")

            pasaporte_vigente = self.consola.leer_booleano(
                "¿Pasaporte vigente? (s/n): "
            )

            tiene_visa = self.consola.leer_booleano("¿Tiene visa? (s/n): ")

            visa_vigente = self.consola.leer_booleano("¿Visa vigente? (s/n): ")

            check_in_realizado = self.consola.leer_booleano(
                "¿Check-in realizado? (s/n): "
            )

            boleto_valido = self.consola.leer_booleano("¿Boleto válido? (s/n): ")

            print("\nEQUIPAJE")

            cantidad_maletas = self.consola.leer_entero("Cantidad de maletas: ")

            peso_total = 0.0
            largo = 0.0
            ancho = 0.0
            alto = 0.0

            preguntas_objetos_no_permitidos = (
                ("elementos_peligrosos", "¿Elementos peligrosos? (s/n): "),
                ("material_inflamable", "¿Material inflamable? (s/n): "),
                ("armas", "¿Armas? (s/n): "),
            )

            def leer_objetos_no_permitidos() -> dict:
                return {
                    clave: self.consola.leer_booleano(pregunta)
                    for clave, pregunta in preguntas_objetos_no_permitidos
                }

            if cantidad_maletas > 0:
                peso_total = self.consola.leer_decimal("Peso total (kg): ")

                largo = self.consola.leer_decimal("Largo (cm): ")

                ancho = self.consola.leer_decimal("Ancho (cm): ")

                alto = self.consola.leer_decimal("Alto (cm): ")

            objetos_no_permitidos = leer_objetos_no_permitidos()

            """Este bloque de código crea instancias de las clases Pasajero, Documento y Equipaje utilizando los datos ingresados por el usuario.
            Luego, se llama al método validar_pasajero del validador para verificar si el pasajero cumple con los requisitos necesarios.
            Dependiendo del resultado de la validación, se agrega el pasajero a la lista de aprobados o rechazados, y se muestra un mensaje correspondiente en la consola."""

            pasajero = Pasajero(
                nombre, edad, nacionalidad, tipo_sangre, telefono, correo, destino
            )

            documento = Documento(
                numero_pasaporte,
                pasaporte_vigente,
                tiene_visa,
                visa_vigente,
                check_in_realizado,
                boleto_valido,
            )

            equipaje = Equipaje(
                cantidad_maletas,
                peso_total,
                largo,
                ancho,
                alto,
                **objetos_no_permitidos,
            )

            aprobado, motivo = self.validador.validar_pasajero(
                pasajero, documento, equipaje
            )

            if aprobado:
                # Agrega el pasajero a la lista de aprobados
                self.aprobados.append((pasajero, equipaje))

                print("\n PASAJERO APROBADO")

                if equipaje.en_bodega:
                    print("Equipaje enviado a bodega.")
                    print(f"Cargo adicional: ${equipaje.cargo_adicional:,.0f}")

            else:
                # Agrega el pasajero a la lista de rechazados junto con los motivos del rechazo
                self.rechazados.append((pasajero, "\n-".join(motivo)))

                print("\n PASAJERO RECHAZADO")
                print("Motivos de rechazo:", motivo)

    def mostrar_reporte(self) -> None:

        print("\n" + "=" * 60)
        print("REPORTE FINAL")
        print("=" * 60)

        if self.aprobados:
            print("\nPASAJEROS APROBADOS")
            # Muestra la lista de pasajeros aprobados junto con el cargo adicional por equipaje, si corresponde.
            for indice, dato in enumerate(self.aprobados, start=1):
                pasajero = dato[0]
                equipaje = dato[1]

                print(
                    f"""{indice}. {pasajero.nombre} - {pasajero.destino} | Cargo: $ {equipaje.cargo_adicional:,.0f}"""
                )
        if self.rechazados:
            print("\n PASAJEROS RECHAZADOS")
            # Muestra la lista de pasajeros rechazados junto con el motivo del rechazo.
            for indice, (pasajero, motivos) in enumerate(self.rechazados, start=1):
                print(f"""{indice}. {pasajero.nombre} - {pasajero.destino} \n Motivos: {motivos}""")


def main():
    sistema = SistemaAeropuerto()

    sistema.registrar_pasajero()

    sistema.mostrar_reporte()


if __name__ == "__main__":
    main()
