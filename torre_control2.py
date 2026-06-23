# ══════════════════════════════════════════════════════════════
#  TORRE DE CONTROL  
#  Se integra con sistema_aeropuerto.py
# ══════════════════════════════════════════════════════════════

from aeropuerto_v21 import (
    SistemaAeropuerto,
    SistemaConsultas
)


# ── Modelos de datos ───────────────────────────────────────────

class Piloto:

    def __init__(
        self,
        nombre: str,
        licencia: str,
        horas_vuelo: int,
        disponible: bool
    ) -> None:

        self.nombre      = nombre
        self.licencia    = licencia
        self.horas_vuelo = horas_vuelo
        self.disponible  = disponible


class Aeronave:

    def __init__(
        self,
        matricula: str,
        modelo: str,
        capacidad: int,
        disponible: bool
    ) -> None:

        self.matricula  = matricula
        self.modelo     = modelo
        self.capacidad  = capacidad
        self.disponible = disponible


class Vuelo:

    def __init__(
        self,
        codigo: str,
        origen: str,
        destino: str,
        cantidad_pasajeros: int
    ) -> None:

        self.codigo             = codigo
        self.origen             = origen
        self.destino            = destino
        self.cantidad_pasajeros = cantidad_pasajeros
        self.estado             = "Pendiente"
        self.piloto:   Piloto   | None = None
        self.aeronave: Aeronave | None = None


# ── Validaciones ───────────────────────────────────────────────

class ControladorAereo:

    HORAS_MINIMAS = 500

    def verificar_piloto(
        self,
        piloto: Piloto
    ) -> tuple[bool, str]:

        if not piloto.disponible:
            return False, "Piloto no disponible"

        if piloto.horas_vuelo < self.HORAS_MINIMAS:
            return (
                False,
                f"Pocas horas de experiencia "
                f"(mínimo {self.HORAS_MINIMAS})"
            )

        return True, "Piloto aprobado"

    def verificar_aeronave(
        self,
        aeronave: Aeronave
    ) -> tuple[bool, str]:

        if not aeronave.disponible:
            return False, "Aeronave no disponible"

        return True, "Aeronave aprobada"

    def verificar_capacidad(
        self,
        vuelo: Vuelo,
        aeronave: Aeronave
    ) -> tuple[bool, str]:

        if vuelo.cantidad_pasajeros > aeronave.capacidad:
            return (
                False,
                f"Capacidad excedida "
                f"({vuelo.cantidad_pasajeros} pax / "
                f"capacidad {aeronave.capacidad})"
            )

        return True, "Capacidad aprobada"

    def verificar_clima(
        self,
        clima_favorable: bool
    ) -> tuple[bool, str]:

        if not clima_favorable:
            return False, "Clima desfavorable"

        return True, "Clima favorable"

    def verificar_pista(
        self,
        pista_libre: bool
    ) -> tuple[bool, str]:

        if not pista_libre:
            return False, "Pista ocupada"

        return True, "Pista libre"

    def verificar_combustible(
        self,
        combustible_suficiente: bool
    ) -> tuple[bool, str]:

        if not combustible_suficiente:
            return False, "Combustible insuficiente"

        return True, "Combustible OK"

    def autorizar_despegue(
        self,
        vuelo: Vuelo,
        piloto: Piloto,
        aeronave: Aeronave,
        clima_favorable: bool,
        pista_libre: bool,
        combustible_suficiente: bool
    ) -> tuple[bool, list]:

        print("\n" + "=" * 60)
        print("  VERIFICACIONES DE CONTROL AÉREO")
        print("=" * 60)

        motivos_rechazo = []

        # Verificar piloto
        valido, mensaje = self.verificar_piloto(piloto)
        print(f"  Piloto:        {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        # Verificar aeronave
        valido, mensaje = self.verificar_aeronave(aeronave)
        print(f"  Aeronave:      {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        # Verificar capacidad
        valido, mensaje = self.verificar_capacidad(vuelo, aeronave)
        print(f"  Capacidad:     {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        # Verificar clima
        valido, mensaje = self.verificar_clima(clima_favorable)
        print(f"  Clima:         {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        # Verificar pista
        valido, mensaje = self.verificar_pista(pista_libre)
        print(f"  Pista:         {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        # Verificar combustible
        valido, mensaje = self.verificar_combustible(combustible_suficiente)
        print(f"  Combustible:   {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        # Resultado final
        if len(motivos_rechazo) == 0:

            vuelo.estado  = "Autorizado"
            vuelo.piloto  = piloto
            vuelo.aeronave = aeronave
            return True, []

        else:

            vuelo.estado = "Denegado"
            return False, motivos_rechazo


# ── Consultas de vuelos ────────────────────────────────────────

class ConsultasVuelos:

    def __init__(self, vuelos: list) -> None:
        self.vuelos = vuelos

    def mostrar_todos(self) -> None:

        print("\nHISTORIAL DE VUELOS")

        if not self.vuelos:
            print("  (ningún vuelo registrado)")
            return

        for i, vuelo in enumerate(self.vuelos, 1):
            print(
                f"  {i}. [{vuelo.estado}] "
                f"{vuelo.codigo} | "
                f"{vuelo.origen} → {vuelo.destino} | "
                f"{vuelo.cantidad_pasajeros} pax"
            )

    def mostrar_autorizados(self) -> None:

        print("\nVUELOS AUTORIZADOS")

        autorizados = [
            v for v in self.vuelos
            if v.estado == "Autorizado"
        ]

        if not autorizados:
            print("  (ninguno)")
            return

        for i, vuelo in enumerate(autorizados, 1):

            nombre_piloto = "Sin asignar"

            if vuelo.piloto is not None:
                nombre_piloto = vuelo.piloto.nombre

            modelo_aeronave = "Sin asignar"

            if vuelo.aeronave is not None:
                modelo_aeronave = vuelo.aeronave.modelo

            print(
                f"  {i}. {vuelo.codigo} | "
                f"{vuelo.origen} → {vuelo.destino}"
            )

            print(
                f"     Piloto:   {nombre_piloto} | "
                f"Aeronave: {modelo_aeronave}"
            )

            print(
                f"     Pasajeros: {vuelo.cantidad_pasajeros}"
            )

    def mostrar_denegados(self) -> None:

        print("\nVUELOS DENEGADOS")

        denegados = [
            v for v in self.vuelos
            if v.estado == "Denegado"
        ]

        if not denegados:
            print("  (ninguno)")
            return

        for i, vuelo in enumerate(denegados, 1):
            print(
                f"  {i}. {vuelo.codigo} | "
                f"{vuelo.origen} → {vuelo.destino} | "
                f"{vuelo.cantidad_pasajeros} pax"
            )

    def buscar_vuelo(self) -> None:

        codigo = input("Código de vuelo a buscar: ").strip().upper()

        for vuelo in self.vuelos:

            if vuelo.codigo.upper() == codigo:

                print("\n── FICHA DE VUELO ──")
                print(f"  Código:     {vuelo.codigo}")
                print(f"  Origen:     {vuelo.origen}")
                print(f"  Destino:    {vuelo.destino}")
                print(f"  Pasajeros:  {vuelo.cantidad_pasajeros}")
                print(f"  Estado:     {vuelo.estado}")

                if vuelo.piloto is not None:
                    print(f"  Piloto:     {vuelo.piloto.nombre}")
                    print(f"  Licencia:   {vuelo.piloto.licencia}")
                    print(f"  Horas vuelo:{vuelo.piloto.horas_vuelo}")

                if vuelo.aeronave is not None:
                    print(f"  Aeronave:   {vuelo.aeronave.modelo}")
                    print(f"  Matrícula:  {vuelo.aeronave.matricula}")
                    print(f"  Capacidad:  {vuelo.aeronave.capacidad}")

                return

        print("  Vuelo no encontrado.")

    def filtrar_por_destino(self) -> None:

        destino = input("Destino a filtrar: ").strip().lower()

        resultados = [
            v for v in self.vuelos
            if v.destino.lower() == destino
        ]

        print(f"\nVUELOS CON DESTINO: {destino.upper()}")

        if not resultados:
            print("  (ninguno)")
            return

        for i, v in enumerate(resultados, 1):
            print(
                f"  {i}. [{v.estado}] "
                f"{v.codigo} — {v.cantidad_pasajeros} pax"
            )

    def mostrar_estadisticas(self) -> None:

        total       = len(self.vuelos)
        autorizados = len([v for v in self.vuelos if v.estado == "Autorizado"])
        denegados   = len([v for v in self.vuelos if v.estado == "Denegado"])
        pendientes  = len([v for v in self.vuelos if v.estado == "Pendiente"])

        total_pasajeros = sum(
            v.cantidad_pasajeros
            for v in self.vuelos
            if v.estado == "Autorizado"
        )

        print("\n" + "═" * 45)
        print("  ESTADÍSTICAS DE VUELOS")
        print("═" * 45)
        print(f"  Total vuelos:        {total}")
        print(f"  Autorizados:         {autorizados}")
        print(f"  Denegados:           {denegados}")
        print(f"  Pendientes:          {pendientes}")

        if total > 0:
            pct = autorizados / total * 100
            print(f"  Tasa autorización:   {pct:.1f}%")

        print(f"  Pasajeros en vuelo:  {total_pasajeros}")
        print("═" * 45)


# ── Sistema de torre de control ────────────────────────────────

class SistemaTorreControl:

    def __init__(self, pasajeros_aprobados: list) -> None:

        self.pasajeros_aprobados = pasajeros_aprobados
        self.vuelos: list[Vuelo] = []
        self.controlador         = ControladorAereo()

    def _leer_texto(self, mensaje: str) -> str:
        return input(mensaje).strip()

    def _leer_entero(self, mensaje: str) -> int:

        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print("  ✘ Ingrese un número entero válido.")

    def _leer_booleano(self, mensaje: str) -> bool:

        while True:
            respuesta = input(mensaje).strip().lower()
            if respuesta in ("s", "n"):
                return respuesta == "s"
            print("  ✘ Responda 's' o 'n'.")

    def registrar_vuelo(self) -> None:

        print("\n" + "═" * 60)
        print("  REGISTRO DE VUELO")
        print("═" * 60)

        # ── Integración con el sistema de aeropuerto ──────────
        # Se toma la cantidad de pasajeros aprobados
        # automáticamente desde el sistema de aeropuerto

        cantidad_pasajeros = len(self.pasajeros_aprobados)

        print(
            f"\n  Pasajeros aprobados del sistema: "
            f"{cantidad_pasajeros}"
        )

        print("\nDATOS DEL VUELO")

        codigo  = self._leer_texto("Código del vuelo: ").upper()
        origen  = self._leer_texto("Origen: ")
        destino = self._leer_texto("Destino: ")

        print("\nDATOS DEL PILOTO")

        nombre_piloto    = self._leer_texto("Nombre: ")
        licencia         = self._leer_texto("Licencia: ")
        horas_vuelo      = self._leer_entero("Horas de vuelo: ")
        piloto_disponible = self._leer_booleano("¿Disponible? (s/n): ")

        print("\nDATOS DE LA AERONAVE")

        matricula          = self._leer_texto("Matrícula: ").upper()
        modelo             = self._leer_texto("Modelo: ")
        capacidad          = self._leer_entero("Capacidad máxima: ")
        aeronave_disponible = self._leer_booleano("¿Disponible? (s/n): ")

        print("\nCONDICIONES")

        clima_favorable        = self._leer_booleano("¿Clima favorable? (s/n): ")
        pista_libre            = self._leer_booleano("¿Pista libre? (s/n): ")
        combustible_suficiente = self._leer_booleano("¿Combustible suficiente? (s/n): ")

        # Crear objetos
        piloto = Piloto(
            nombre_piloto,
            licencia,
            horas_vuelo,
            piloto_disponible
        )

        aeronave = Aeronave(
            matricula,
            modelo,
            capacidad,
            aeronave_disponible
        )

        vuelo = Vuelo(
            codigo,
            origen,
            destino,
            cantidad_pasajeros
        )

        # Autorizar
        autorizado, motivos = self.controlador.autorizar_despegue(
            vuelo,
            piloto,
            aeronave,
            clima_favorable,
            pista_libre,
            combustible_suficiente
        )

        print("\n" + "=" * 60)

        if autorizado:

            print("  ✔ DESPEGUE AUTORIZADO")
            print(f"  Vuelo {vuelo.codigo}: {vuelo.origen} → {vuelo.destino}")
            print(f"  Pasajeros a bordo: {vuelo.cantidad_pasajeros}")

        else:

            print("  ✘ DESPEGUE DENEGADO")
            print("  Motivos:")

            for motivo in motivos:
                print(f"    • {motivo}")

        print("=" * 60)

        self.vuelos.append(vuelo)

    def exportar_reporte(self) -> None:

        nombre_archivo = "reporte_torre_control.txt"

        autorizados = [v for v in self.vuelos if v.estado == "Autorizado"]
        denegados   = [v for v in self.vuelos if v.estado == "Denegado"]

        lineas = [
            "=" * 60,
            "  REPORTE TORRE DE CONTROL",
            "=" * 60,
            "",
            f"Total vuelos registrados : {len(self.vuelos)}",
            f"Autorizados              : {len(autorizados)}",
            f"Denegados                : {len(denegados)}",
            "",
            "─" * 60,
            "VUELOS AUTORIZADOS",
            "─" * 60,
        ]

        for i, v in enumerate(autorizados, 1):

            nombre_piloto = "Sin asignar"

            if v.piloto is not None:
                nombre_piloto = v.piloto.nombre

            lineas.append(
                f"{i:>3}. {v.codigo:<10} "
                f"{v.origen:<15} → {v.destino:<15} "
                f"| {v.cantidad_pasajeros} pax "
                f"| Piloto: {nombre_piloto}"
            )

        lineas += ["", "─" * 60, "VUELOS DENEGADOS", "─" * 60]

        for i, v in enumerate(denegados, 1):
            lineas.append(
                f"{i:>3}. {v.codigo:<10} "
                f"{v.origen:<15} → {v.destino:<15} "
                f"| {v.cantidad_pasajeros} pax"
            )

        lineas += ["", "=" * 60]

        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))

        print(f"\n  ✔ Reporte exportado como '{nombre_archivo}'")


# ══════════════════════════════════════════════════════════════
#  PROGRAMA PRINCIPAL
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # ── Paso 1: sistema de aeropuerto ─────────────────────────

    sistema = SistemaAeropuerto()

    cantidad = sistema.consola.leer_entero(
        "¿Cuántos pasajeros desea registrar?: "
    )

    for _ in range(cantidad):
        sistema.registrar_pasajero()

    sistema.mostrar_reporte()

    # ── Paso 2: torre de control ───────────────────────────────

    torre = SistemaTorreControl(sistema.aprobados)

    print("\n" + "═" * 60)
    print("  TORRE DE CONTROL")
    print("═" * 60)

    cantidad_vuelos = torre._leer_entero(
        "¿Cuántos vuelos desea registrar?: "
    )

    for _ in range(cantidad_vuelos):
        torre.registrar_vuelo()

    # ── Paso 3: menú de consultas ──────────────────────────────

    consultas_aeropuerto = SistemaConsultas(
        sistema.aprobados,
        sistema.rechazados
    )

    consultas_vuelos = ConsultasVuelos(torre.vuelos)

    MENU = """
╔══════════════════════════════════════╗
║          MENÚ PRINCIPAL              ║
╠══════════════════════════════════════╣
║  ── AEROPUERTO ─────────────────────║
║   1. Ver pasajeros aprobados         ║
║   2. Ver pasajeros rechazados        ║
║   3. Buscar pasajero                 ║
║   4. Filtrar por destino             ║
║   5. Filtrar por nacionalidad        ║
║   6. Filtrar por rango de edad       ║
║   7. Equipaje en bodega              ║
║   8. Pasajeros sin cargo             ║
║   9. Destinos frecuentes             ║
║  10. Estadísticas de pasajeros       ║
║  11. Exportar reporte aeropuerto     ║
║  ── TORRE DE CONTROL ───────────────║
║  12. Ver todos los vuelos            ║
║  13. Ver vuelos autorizados          ║
║  14. Ver vuelos denegados            ║
║  15. Buscar vuelo por código         ║
║  16. Filtrar vuelos por destino      ║
║  17. Estadísticas de vuelos          ║
║  18. Exportar reporte torre          ║
║  ─────────────────────────────────── ║
║   0. Salir                           ║
╚══════════════════════════════════════╝"""

    ACCIONES = {
        "1":  consultas_aeropuerto.mostrar_aprobados,
        "2":  consultas_aeropuerto.mostrar_rechazados,
        "3":  consultas_aeropuerto.buscar_pasajero,
        "4":  consultas_aeropuerto.filtrar_por_destino,
        "5":  consultas_aeropuerto.filtrar_por_nacionalidad,
        "6":  consultas_aeropuerto.filtrar_por_edad,
        "7":  consultas_aeropuerto.mostrar_bodega,
        "8":  consultas_aeropuerto.mostrar_sin_cargo,
        "9":  consultas_aeropuerto.mostrar_destinos,
        "10": consultas_aeropuerto.mostrar_estadisticas,
        "11": consultas_aeropuerto.exportar_reporte,
        "12": consultas_vuelos.mostrar_todos,
        "13": consultas_vuelos.mostrar_autorizados,
        "14": consultas_vuelos.mostrar_denegados,
        "15": consultas_vuelos.buscar_vuelo,
        "16": consultas_vuelos.filtrar_por_destino,
        "17": consultas_vuelos.mostrar_estadisticas,
        "18": torre.exportar_reporte,
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
