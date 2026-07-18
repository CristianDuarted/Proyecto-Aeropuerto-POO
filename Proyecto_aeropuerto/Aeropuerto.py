"""Este programa simula un sistema de control de pasajeros en un aeropuerto.
Permite registrar información de pasajeros, validar sus documentos y equipaje
y generar un reporte final indicando los pasajeros aprobados y rechazados."""

from pathlib import Path
from collections import Counter


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
        maletas: list | None = None,
    ) -> None:

        self.cantidad_maletas = cantidad_maletas
        self.peso_total = peso_total
        self.largo = largo
        self.ancho = ancho
        self.alto = alto
        self.elementos_peligrosos = elementos_peligrosos
        self.material_inflamable = material_inflamable
        self.armas = armas
        self.maletas = maletas if maletas is not None else []
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

        if equipaje.cantidad_maletas > 3:
            exceso = equipaje.cantidad_maletas - 3
            equipaje.cargo_adicional += exceso * 50000.0
            equipaje.en_bodega = True

        if equipaje.peso_total > 23.0:
            equipaje.cargo_adicional += (equipaje.peso_total - 23.0) * 10000.0
            equipaje.en_bodega = True

        # Evalua las dimensiones de CADA maleta individualmente
        for i, maleta in enumerate(equipaje.maletas, 1):
            if maleta["largo"] > 55 or maleta["ancho"] > 40 or maleta["alto"] > 25:
                equipaje.cargo_adicional += 50000.0
                equipaje.en_bodega = True
                print(f"  Maleta {i}: dimensiones exceden el limite, cargo $50.000")


class SistemaConsultas:
    def __init__(self, aprobados: list, rechazados: list) -> None:
        self.aprobados = aprobados
        self.rechazados = rechazados

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

        nombre = input("Nombre a buscar: ").strip().lower()

        for pasajero, equipaje in self.aprobados:
            if pasajero.nombre.lower() == nombre:
                self._mostrar_ficha_aprobado(pasajero, equipaje)
                return

        for pasajero, motivo in self.rechazados:
            if pasajero.nombre.lower() == nombre:
                self._mostrar_ficha_rechazado(pasajero, motivo)
                return

        print("  Pasajero no encontrado.")

    def _mostrar_ficha_aprobado(self, pasajero, equipaje) -> None:

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

    def _mostrar_ficha_rechazado(self, pasajero, motivo: str) -> None:

        print("\n── FICHA PASAJERO (RECHAZADO) ──")
        print(f"  Nombre:       {pasajero.nombre}")
        print(f"  Edad:         {pasajero.edad} años")
        print(f"  Nacionalidad: {pasajero.nacionalidad}")
        print(f"  Destino:      {pasajero.destino}")
        print(f"  Motivo:       {motivo}")

    # ── Filtros ────────────────────────────────────────────────

    def filtrar_por_destino(self) -> None:

        destino = input("Destino a filtrar: ").strip().lower()

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

        nacionalidad = input("Nacionalidad a filtrar: ").strip().lower()

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
            print(f"    • {p.nombre}  ({m})")

    def filtrar_por_edad(self) -> None:

        print("Rango de edad:")
        try:
            edad_min = int(input("  Desde: "))
            edad_max = int(input("  Hasta: "))
        except ValueError:
            print("  Error, ingresa solo números enteros.")
            return

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

        destinos = [p.destino for p, _ in self.aprobados]
        destino_top = Counter(destinos).most_common(1)

        mayor = max(self.aprobados, key=lambda x: x[1].cargo_adicional, default=None)

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
        carpeta_paquete = Path("Proyecto_aeropuerto")
        carpeta_Reportes = Path("Reportes")
        carpeta_aeropuerto = Path("reporte_aeropuerto")

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
            lineas.append(f"{i:>3}. {p.nombre:<25}  motivo: {m}")

        lineas += ["", "=" * 60]
        carpeta_Reportes = carpeta_paquete / "Reportes"
        carpeta_aeropuerto = carpeta_Reportes / "Aeropuerto"
        carpeta_aeropuerto.mkdir(parents=True, exist_ok=True)
        nombre_archivo = carpeta_aeropuerto / "reporte_aeropuerto.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))

        print(f"\n  ✔ Reporte exportado como '{nombre_archivo}'")
