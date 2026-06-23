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
        return float(input(mensaje))

    def leer_booleano(self, mensaje: str) -> bool:
        respuesta = input(mensaje).strip().lower()
        return respuesta == "s"


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


class ValidadorPasajero:
    def validar_pasajero(
        self, pasajero: Pasajero, documento: Documento, equipaje: Equipaje
    ) -> tuple[bool, str]:

        if pasajero.edad < 18:
            return False, "Menor de edad"

        if not documento.pasaporte_vigente:
            return False, "Pasaporte vencido"

        paises_con_visa = ["canada", "estados unidos", "australia", "reino unido"]

        if pasajero.destino.lower() in paises_con_visa:
            if not documento.tiene_visa:
                return False, "El destino requiere visa"

            if not documento.visa_vigente:
                return False, "Visa vencida"

        if not documento.check_in_realizado:
            return False, "No realizó check-in"

        if not documento.boleto_valido:
            return False, "Boleto inválido"

        if equipaje.armas:
            return False, "Transporta armas"

        if equipaje.material_inflamable:
            return False, "Material inflamable"

        if equipaje.elementos_peligrosos:
            return False, "Elementos peligrosos"

        self.validar_equipaje(equipaje)

        return True, "Aprobado"

    def validar_equipaje(self, equipaje: Equipaje) -> None:

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


class SistemaAeropuerto:
    def __init__(self) -> None:

        self.aprobados: list[tuple[Pasajero, Equipaje]] = []
        self.rechazados: list[tuple[Pasajero, str]] = []

        self.consola = Consola()
        self.validador = ValidadorPasajero()

    def registrar_pasajero(self) -> None:

        cantidad = self.consola.leer_entero("¿Cuántos pasajeros desea registrar?: ")
        for _ in range(cantidad):
            print("\n" + "=" * 60)
            print(
                f"REGISTRO DE PASAJERO N° {len(self.aprobados) + len(self.rechazados) + 1}"
            )
            print("=" * 60)

            nombre = self.consola.leer_texto("Nombre: ")
            edad = self.consola.leer_entero("Edad: ")
            nacionalidad = self.consola.leer_texto("Nacionalidad: ")
            for caracter in nacionalidad:
                codigo = ord(caracter)  # ord() da el valor ASCII
                # Letras mayúsculas: 65-90, minúsculas: 97-122, espacio: 32
                if (65 <= codigo <= 90) or (97 <= codigo <= 122) or codigo == 32:
                    nacionalidad += caracter
                else:
                    print(
                        "Error, ingresa solo letras (con espacios si llega ser el caso), por favor"
                    )
                    nacionalidad = self.consola.leer_texto("Nacionalidad: ")
            Tipo_sangre = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
            tipo_sangre = self.consola.leer_texto("Tipo de sangre: ")
            while True:
                if tipo_sangre in Tipo_sangre:
                    break
                else:
                    print("Error, ingresa el tipo de sangre correcto, por favor")
                    tipo_sangre = self.consola.leer_texto("Tipo de sangre: ")
            telefono = self.consola.leer_texto("Teléfono: ")
            correo = self.consola.leer_texto("Correo: ")
            destino = self.consola.leer_texto("Destino: ")
            for caracter in destino:
                codigo = ord(caracter)  # ord() da el valor ASCII
                # Letras mayúsculas: 65-90, minúsculas: 97-122, espacio: 32
                if (65 <= codigo <= 90) or (97 <= codigo <= 122) or codigo == 32:
                    destino += caracter
                else:
                    print(
                        "Error, ingresa solo letras (con espacios si llega ser el caso), por favor"
                    )
                    destino = self.consola.leer_texto("Destino: ")

            print("\nDOCUMENTOS")

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

            peso_total = self.consola.leer_decimal("Peso total (kg): ")

            largo = self.consola.leer_decimal("Largo (cm): ")

            ancho = self.consola.leer_decimal("Ancho (cm): ")

            alto = self.consola.leer_decimal("Alto (cm): ")

            elementos_peligrosos = self.consola.leer_booleano(
                "¿Elementos peligrosos? (s/n): "
            )

            material_inflamable = self.consola.leer_booleano(
                "¿Material inflamable? (s/n): "
            )

            armas = self.consola.leer_booleano("¿Armas? (s/n): ")

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
                elementos_peligrosos,
                material_inflamable,
                armas,
            )

            aprobado, motivo = self.validador.validar_pasajero(
                pasajero, documento, equipaje
            )

            if aprobado:
                self.aprobados.append((pasajero, equipaje))

                print("\n PASAJERO APROBADO")

                if equipaje.en_bodega:
                    print("Equipaje enviado a bodega.")
                    print(f"Cargo adicional: ${equipaje.cargo_adicional:,.0f}")

            else:
                self.rechazados.append((pasajero, motivo))

                print("\n PASAJERO RECHAZADO")
                print("Motivo:", motivo)

    def mostrar_reporte(self) -> None:

        print("\n" + "=" * 60)
        print("REPORTE FINAL")
        print("=" * 60)

        if not self.rechazados:
            print("\nPASAJEROS APROBADOS")

            for indice, dato in enumerate(self.aprobados, start=1):
                pasajero = dato[0]
                equipaje = dato[1]

                print(
                    f"""{indice}. "
                    {pasajero.nombre} "
                    - {pasajero.destino}"
                    Cargo: "
                    ${equipaje.cargo_adicional:,.0f}"""
                )
        if self.rechazados:
            print("\n PASAJEROS RECHAZADOS")

            for indice, (pasajero, motivo) in enumerate(self.rechazados, start=1):
                print(f"""{indice}.
                       {pasajero.nombre}
                             Motivo: {motivo}""")


def main():
    sistema = SistemaAeropuerto()

    sistema.registrar_pasajero()

    sistema.mostrar_reporte()


if __name__ == "__main__":
    main()
