"""Este programa simula un sistema de control de pasajeros en un aeropuerto.
Permite registrar información de pasajeros, validar sus documentos y equipaje
y generar un reporte final indicando los pasajeros aprobados y rechazados."""

from collections import Counter
import re  # Sirve para validar los datos de entrada del usuario, como nombres, correos electrónicos y números de teléfono.


# ── Utilidades de consola ──────────────────────────────────────
# Se usa para leer datos de entrada del usuario desde la consola y para mostrar mensajes de salida en la consola.
class Consola:
    def leer_texto(self, mensaje: str) -> str:
        return input(mensaje).strip()

    def leer_entero(self, mensaje: str) -> int:
        while True:
            try:
                valor = int(input(mensaje))
                return valor
            except ValueError:
                print("Error, ingresa un número entero válido, por favor")

    def leer_decimal(self, mensaje: str) -> float:
        while True:
            try:
                valor = float(input(mensaje))
                return valor
            except ValueError:
                print("Error, ingresa un número decimal válido, por favor")

    def leer_booleano(self, mensaje: str) -> bool:
        while True:
            respuesta = input(mensaje).strip().lower()
            if respuesta in ["s", "n"]:
                return respuesta == "s"
            print("Error, ingresa solo s o n, por favor")

    def validacion(self, mensaje: str, patron: str | list[str]) -> str:
        # Permite eliminar espacios en blanco al inicio y al final de la cadena antes de realizar la validación.
        # Luego, se utiliza re.match() para verificar si cumple con la expresión regular definida en patron.
        while True:
            respuesta = self.leer_texto(mensaje)
            if isinstance(patron, str):
                if re.match(patron, respuesta):
                    return respuesta
            if isinstance(patron, list):
                if respuesta.upper() in patron:
                    return respuesta.upper()
            print("Error, ingresa el dato correctamente, por favor")

    def leer_decimal_positivo(self, mensaje: str) -> float:
        while True:
            valor = self.leer_decimal(mensaje)
            if valor > 0:
                return valor
            print("Error, ingresa el dato correctamente, por favor")


# ── Modelos de datos ───────────────────────────────────────────
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


# ── Validación ─────────────────────────────────────────────────
# Esta clase se encarga de validar la información de un pasajero, sus documentos y su equipaje.
# Si el pasajero es aprobado, también calcula los cargos adicionales por exceso de equipaje o dimensiones fuera de los límites permitidos.
class ValidadorPasajero:
    PAISES_CON_VISA = ["canada", "estados unidos", "australia", "reino unido"]

    def validar_pasajero(
        self, pasajero: Pasajero, documento: Documento, equipaje: Equipaje
    ) -> tuple[bool, list[str]]:

        motivos_rechazo = []
        motivos_aprobado = []

        if pasajero.edad < 18:
            motivos_rechazo.append("Menor de edad")

        if not documento.pasaporte_vigente:
            motivos_rechazo.append("Pasaporte vencido")

        if pasajero.destino.lower() in self.PAISES_CON_VISA:
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


# ── Consultas y reportes ───────────────────────────────────────


class SistemaConsultas:
    def __init__(self, aprobados: list, rechazados: list) -> None:
        self.aprobados = aprobados
        self.rechazados = rechazados
        self.consola = Consola()

    # ── Listados básicos ───────────────────────────────────────

    def mostrar_aprobados(self) -> None:

        print("\nPASAJEROS APROBADOS")

        if not self.aprobados:
            print("  (ninguno)")
            return

        for i, (pasajero, equipaje) in enumerate(self.aprobados, 1):
            cargo = (
                f"  cargo: ${equipaje.cargo_adicional:,.0f}"
                if equipaje.cargo_adicional
                else ""
            )
            print(f"  {i}. {pasajero.nombre} → {pasajero.destino}{cargo}")

    def mostrar_rechazados(self) -> None:

        print("\nPASAJEROS RECHAZADOS")

        if not self.rechazados:
            print("  (ninguno)")
            return

        for i, (pasajero, motivo) in enumerate(self.rechazados, 1):
            print(f"  {i}. {pasajero.nombre}  |  Motivo: {motivo}")

    # ── Búsqueda ───────────────────────────────────────────────

    def buscar_pasajero(self) -> None:

        nombre = self.consola.leer_texto("Nombre a buscar: ").lower()

        for pasajero, equipaje in self.aprobados:
            if pasajero.nombre.lower() == nombre:
                self._mostrar_ficha_aprobado(pasajero, equipaje)
                return

        for pasajero, motivo in self.rechazados:
            if pasajero.nombre.lower() == nombre:
                self._mostrar_ficha_rechazado(pasajero, motivo)
                return

        print("  Pasajero no encontrado.")

    def _mostrar_ficha_aprobado(self, pasajero: Pasajero, equipaje: Equipaje) -> None:

        print("\n── FICHA PASAJERO (APROBADO) ──")
        print(f"  Nombre:       {pasajero.nombre}")
        print(f"  Edad:         {pasajero.edad} años")
        print(f"  Nacionalidad: {pasajero.nacionalidad}")
        print(f"  Destino:      {pasajero.destino}")
        print(f"  Teléfono:     {pasajero.telefono}")
        print(f"  Correo:       {pasajero.correo}")
        print(f"  Tipo sangre:  {pasajero.tipo_sangre}")
        print(
            f"  Maletas:      {equipaje.cantidad_maletas}  |  Peso: {equipaje.peso_total} kg"
        )
        print(f"  En bodega:    {'Sí' if equipaje.en_bodega else 'No'}")
        print(f"  Cargo extra:  ${equipaje.cargo_adicional:,.0f}")

    def _mostrar_ficha_rechazado(self, pasajero: Pasajero, motivo: str) -> None:

        print("\n── FICHA PASAJERO (RECHAZADO) ──")
        print(f"  Nombre:       {pasajero.nombre}")
        print(f"  Edad:         {pasajero.edad} años")
        print(f"  Nacionalidad: {pasajero.nacionalidad}")
        print(f"  Destino:      {pasajero.destino}")
        print(f"  Motivo:       {motivo}")

    # ── Filtros ────────────────────────────────────────────────

    def filtrar_por_destino(self) -> None:

        destino = self.consola.leer_texto("Destino a filtrar: ").lower()

        resultados = [
            pasajero
            for pasajero, _ in self.aprobados
            if pasajero.destino.lower() == destino
        ]

        print(f"\nPASAJEROS APROBADOS CON DESTINO: {destino.upper()}")

        if not resultados:
            print("  (ninguno)")
            return

        for i, pasajero in enumerate(resultados, 1):
            print(f"  {i}. {pasajero.nombre}")

    def filtrar_por_nacionalidad(self) -> None:

        nacionalidad = self.consola.leer_texto("Nacionalidad a filtrar: ").lower()

        aprobados = [
            p for p, _ in self.aprobados if p.nacionalidad.lower() == nacionalidad
        ]

        rechazados = [
            (p, m) for p, m in self.rechazados if p.nacionalidad.lower() == nacionalidad
        ]

        print(f"\nPASAJEROS DE NACIONALIDAD: {nacionalidad.upper()}")
        print(f"  Aprobados: {len(aprobados)}")

        for p in aprobados:
            print(f"    • {p.nombre} → {p.destino}")

        print(f"  Rechazados: {len(rechazados)}")

        for p, m in rechazados:
            print(f"    • {p.nombre}  {m}")

    def filtrar_por_edad(self) -> None:

        print("Rango de edad:")
        edad_min = self.consola.leer_entero("  Desde: ")
        edad_max = self.consola.leer_entero("  Hasta: ")

        resultados = [
            (pasajero, equipaje)
            for pasajero, equipaje in self.aprobados
            if edad_min <= pasajero.edad <= edad_max
        ]

        print(f"\nAPROBADOS ENTRE {edad_min} Y {edad_max} AÑOS")

        if not resultados:
            print("  (ninguno)")
            return

        for i, (p, _) in enumerate(resultados, 1):
            print(f"  {i}. {p.nombre}  ({p.edad} años) → {p.destino}")

    # ── Bodega ─────────────────────────────────────────────────

    def mostrar_bodega(self) -> None:

        en_bodega = [(p, e) for p, e in self.aprobados if e.en_bodega]

        print("\nEQUIPAJE EN BODEGA")

        if not en_bodega:
            print("  Ningún equipaje en bodega.")
            return

        total = 0

        for p, e in en_bodega:
            print(f"  • {p.nombre}  — ${e.cargo_adicional:,.0f}")
            total += e.cargo_adicional

        print(f"\n  Total recaudado por bodega: ${total:,.0f}")

    # ── Pasajeros sin cargo ────────────────────────────────────

    def mostrar_sin_cargo(self) -> None:

        sin_cargo = [p for p, e in self.aprobados if e.cargo_adicional == 0]

        print("\nPASAJEROS SIN CARGO ADICIONAL")

        if not sin_cargo:
            print("  (ninguno)")
            return

        for i, p in enumerate(sin_cargo, 1):
            print(f"  {i}. {p.nombre} → {p.destino}")

    # ── Estadísticas ───────────────────────────────────────────

    def mostrar_estadisticas(self) -> None:

        total = len(self.aprobados) + len(self.rechazados)
        dinero = sum(e.cargo_adicional for _, e in self.aprobados)
        en_bodega = sum(1 for _, e in self.aprobados if e.en_bodega)

        # Destino más frecuente
        destinos = [p.destino for p, _ in self.aprobados]
        destino_top = Counter(destinos).most_common(1)

        # Mayor cargo
        mayor = max(self.aprobados, key=lambda x: x[1].cargo_adicional, default=None)

        # Motivos de rechazo (contar cada motivo individual)
        motivos: Counter[str] = Counter()
        for _, m in self.rechazados:
            for linea in m.splitlines():
                linea = linea.strip()
                if linea.startswith("- "):
                    motivos[linea[2:]] += 1

        print("\n" + "═" * 45)
        print("  ESTADÍSTICAS")
        print("═" * 45)
        print(f"  Registrados:          {total}")
        print(f"  Aprobados:            {len(self.aprobados)}")
        print(f"  Rechazados:           {len(self.rechazados)}")

        if total > 0:
            pct = len(self.aprobados) / total * 100
            print(f"  Tasa de aprobación:   {pct:.1f}%")

        print(f"  En bodega:            {en_bodega}")
        print(f"  Dinero recaudado:     ${dinero:,.0f}")

        if destino_top:
            print(
                f"  Destino más popular:  {destino_top[0][0]} ({destino_top[0][1]} pax)"
            )

        if mayor and mayor[1].cargo_adicional > 0:
            print(
                f"  Mayor cargo:          "
                f"{mayor[0].nombre} (${mayor[1].cargo_adicional:,.0f})"
            )

        if motivos:
            print("\n  Motivos de rechazo:")
            for motivo, cantidad in motivos.most_common():
                print(f"    • {motivo}: {cantidad}")

        print("═" * 45)

    # ── Destinos frecuentes ────────────────────────────────────

    def mostrar_destinos(self) -> None:

        todos = [p.destino for p, _ in self.aprobados]
        conteo = Counter(todos).most_common()

        print("\nDESTINOS MÁS FRECUENTES")

        if not conteo:
            print("  (sin datos)")
            return

        for destino, cantidad in conteo:
            barra = "█" * cantidad
            print(f"  {destino:<20} {barra} {cantidad}")

    # ── Exportar reporte ───────────────────────────────────────

    def exportar_reporte(self) -> None:

        nombre_archivo = "reporte_aeropuerto.txt"

        total = len(self.aprobados) + len(self.rechazados)
        dinero = sum(e.cargo_adicional for _, e in self.aprobados)

        lineas = [
            "=" * 60,
            "  REPORTE FINAL - SISTEMA AEROPUERTO",
            "=" * 60,
            "",
            f"Total registrados : {total}",
            f"Aprobados         : {len(self.aprobados)}",
            f"Rechazados        : {len(self.rechazados)}",
            f"Dinero recaudado  : ${dinero:,.0f}",
            "",
            "─" * 60,
            "PASAJEROS APROBADOS",
            "─" * 60,
        ]

        for i, (p, e) in enumerate(self.aprobados, 1):
            lineas.append(
                f"{i:>3}. {p.nombre:<25} → {p.destino:<20} "
                f"cargo: ${e.cargo_adicional:,.0f}"
            )

        lineas += ["", "─" * 60, "PASAJEROS RECHAZADOS", "─" * 60]

        for i, (p, m) in enumerate(self.rechazados, 1):
            lineas.append(f"{i:>3}. {p.nombre:<25}")
            lineas.append(f" motivo: {m}")

        lineas += ["", "=" * 60]

        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))

        print(f"\n  ✔ Reporte exportado como '{nombre_archivo}'")


# ── Sistema principal ───────────────────────────────────────


# Esta clase representa el sistema de control de pasajeros en un aeropuerto. Permite registrar pasajeros, validar sus documentos y equipaje.
# Generando un reporte final indicando los pasajeros aprobados y rechazados.
class SistemaAeropuerto:
    # ──────Validación de datos de entrada del usuario────────────────────────
    # Validar nombre (solo letras, espacios, apóstrofes y guiones)
    NOMBRE_REGLA = r"^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s'-]+$"

    # Validar nacionalidad y destino (solo letras y espacios)
    TEXTO_REGLA = r"^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$"

    # Validar tipo de sangre (solo opciones válidas)
    TIPO_SANGRE_REGLA = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

    # Validar teléfono (solo números y espacios, puede iniciar con +)
    TELEFONO_REGLA = r"^\+?[0-9\s]+$"

    # Validar correo (solo direcciones de correo válidas)
    CORREO_REGLA = [
        "unal.edu.co",
        "gmail.com",
        "hotmail.com",
        "icloud.com",
        "outlook.com",
        "yahoo.com",
        "protonmail.com",
    ]

    # Validar pasaporte (solo letras y números)
    PASAPORTE_REGLA = r"^[a-zA-Z0-9]+$"

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

            nombre = self.consola.validacion("Nombre: ", self.NOMBRE_REGLA)
            while True:
                edad = self.consola.leer_entero("Edad: ")
                if edad >= 0:
                    break
                print("Error, la edad no puede ser negativa.")

            nacionalidad = self.consola.validacion("Nacionalidad: ", self.TEXTO_REGLA)
            tipo_sangre = self.consola.validacion(
                "Tipo de sangre: ", self.TIPO_SANGRE_REGLA
            )
            telefono = self.consola.validacion("Teléfono: ", self.TELEFONO_REGLA)

            correo = self.consola.leer_texto("Correo: ")
            # Verifica si el correo ingresado cumple con las condiciones de validación.
            while True:
                # Se eliminan los espacios en blanco al inicio y al final del correo ingresado
                # Se pasa todo a minuscula usando lower()
                correo_limpio = correo.strip().lower()
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
                if dominio not in self.CORREO_REGLA:
                    print("Error, digite correctamente su correo, por favor")
                    correo = self.consola.leer_texto("Correo: ")
                else:
                    correo = correo_limpio
                    break

            destino = self.consola.validacion("Destino: ", self.TEXTO_REGLA)

            print("\nDOCUMENTOS")

            numero_pasaporte = self.consola.validacion(
                "Pasaporte: ", self.PASAPORTE_REGLA
            )
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

            while True:
                cantidad_maletas = self.consola.leer_entero("Cantidad de maletas: ")
                if cantidad_maletas >= 0:
                    break
                print("Error, la cantidad de maletas no puede ser negativa.")

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
                peso_total = self.consola.leer_decimal_positivo("Peso total (kg): ")
                largo = self.consola.leer_decimal_positivo("Largo (cm): ")
                ancho = self.consola.leer_decimal_positivo("Ancho (cm): ")
                alto = self.consola.leer_decimal_positivo("Alto (cm): ")

            objetos_no_permitidos = leer_objetos_no_permitidos()

            # Este bloque de código crea instancias de las clases Pasajero, Documento y Equipaje utilizando los datos ingresados por el usuario.
            # Luego, se llama al método validar_pasajero del validador para verificar si el pasajero cumple con los requisitos necesarios.
            # Dependiendo del resultado de la validación, se agrega el pasajero a la lista de aprobados o rechazados, y se muestra un mensaje correspondiente en la consola.

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
                motivos_formateados = "\n- " + "\n- ".join(motivo)
                self.rechazados.append((pasajero, motivos_formateados))

                print("\n PASAJERO RECHAZADO")
                print("Motivos de rechazo:", motivos_formateados)

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
                print(
                    f"""{indice}. {pasajero.nombre} - {pasajero.destino} \n Motivos: {motivos}"""
                )


# ══════════════════════════════════════════════════════════════
#  PROGRAMA PRINCIPAL
# ══════════════════════════════════════════════════════════════


def main():
    sistema = SistemaAeropuerto()

    sistema.registrar_pasajero()

    sistema.mostrar_reporte()

    consultas = SistemaConsultas(sistema.aprobados, sistema.rechazados)

    MENU = """
╔══════════════════════════════╗
║        MENÚ DE CONSULTAS     ║
╠══════════════════════════════╣
║  1. Ver aprobados            ║
║  2. Ver rechazados           ║
║  3. Buscar pasajero          ║
║  4. Equipaje en bodega       ║
║  5. Estadísticas             ║
║  ── Filtros ─────────────────║
║  6. Filtrar por destino      ║
║  7. Filtrar por nacionalidad ║
║  8. Filtrar por rango de edad║
║  ── Reportes ────────────────║
║  9. Destinos frecuentes      ║
║ 10. Pasajeros sin cargo      ║
║ 11. Exportar reporte (.txt)  ║
║ ─────────────────────────────║
║  0. Salir                    ║
╚══════════════════════════════╝"""

    ACCIONES = {
        "1": consultas.mostrar_aprobados,
        "2": consultas.mostrar_rechazados,
        "3": consultas.buscar_pasajero,
        "4": consultas.mostrar_bodega,
        "5": consultas.mostrar_estadisticas,
        "6": consultas.filtrar_por_destino,
        "7": consultas.filtrar_por_nacionalidad,
        "8": consultas.filtrar_por_edad,
        "9": consultas.mostrar_destinos,
        "10": consultas.mostrar_sin_cargo,
        "11": consultas.exportar_reporte,
    }

    while True:
        print(MENU)

        opcion = input("Opción: ").strip()

        if opcion == "0":
            print("\n  Hasta luego.\n")
            break

        accion = ACCIONES.get(opcion)

        if accion:
            accion()
        else:
            print("  ✘ Opción no válida.")


if __name__ == "__main__":
    main()
