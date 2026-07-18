import sys
from collections import Counter
from pathlib import Path

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))


class Piloto:
    def __init__(
        self,
        nombre: str,
        licencia: str,
        horas_vuelo: int,
        disponible: bool,
    ) -> None:
        self.nombre = nombre
        self.licencia = licencia
        self.horas_vuelo = horas_vuelo
        self.disponible = disponible


class Aeronave:
    def __init__(
        self,
        matricula: str,
        modelo: str,
        capacidad: int,
        disponible: bool,
    ) -> None:
        self.matricula = matricula
        self.modelo = modelo
        self.capacidad = capacidad
        self.disponible = disponible


class Vuelo:
    def __init__(
        self,
        codigo: str,
        origen: str,
        destino: str,
        cantidad_pasajeros: int,
    ) -> None:
        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.cantidad_pasajeros = cantidad_pasajeros
        self.estado = "Pendiente"
        self.piloto: Piloto | None = None
        self.aeronave: Aeronave | None = None


class SolicitudDespegue:
    def __init__(
        self,
        vuelo: Vuelo,
        piloto: Piloto,
        aeronave: Aeronave,
        clima_favorable: bool,
        pista_libre: bool,
        combustible_suficiente: bool,
    ) -> None:
        self.vuelo = vuelo
        self.piloto = piloto
        self.aeronave = aeronave
        self.clima_favorable = clima_favorable
        self.pista_libre = pista_libre
        self.combustible_suficiente = combustible_suficiente


class ControladorAereo:
    HORAS_MINIMAS = 500

    def verificar_piloto(self, piloto: Piloto) -> tuple[bool, str]:
        if not piloto.disponible:
            return False, "Piloto no disponible"
        if piloto.horas_vuelo < self.HORAS_MINIMAS:
            return False, f"Pocas horas de experiencia (minimo {self.HORAS_MINIMAS})"
        return True, "Piloto aprobado"

    def verificar_aeronave(self, aeronave: Aeronave) -> tuple[bool, str]:
        if not aeronave.disponible:
            return False, "Aeronave no disponible"
        return True, "Aeronave aprobada"

    def verificar_capacidad(self, vuelo: Vuelo, aeronave: Aeronave) -> tuple[bool, str]:
        if vuelo.cantidad_pasajeros > aeronave.capacidad:
            return (
                False,
                f"Capacidad excedida ({vuelo.cantidad_pasajeros} pax / capacidad {aeronave.capacidad})",
            )
        return True, "Capacidad aprobada"

    def verificar_clima(self, clima_favorable: bool) -> tuple[bool, str]:
        if not clima_favorable:
            return False, "Clima desfavorable"
        return True, "Clima favorable"

    def verificar_pista(self, pista_libre: bool) -> tuple[bool, str]:
        if not pista_libre:
            return False, "Pista ocupada"
        return True, "Pista libre"

    def verificar_combustible(self, combustible_suficiente: bool) -> tuple[bool, str]:
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
        combustible_suficiente: bool,
    ) -> tuple[bool, list[str]]:
        print("\n" + "=" * 60)
        print("  VERIFICACIONES DE CONTROL AEREO")
        print("=" * 60)

        motivos_rechazo: list[str] = []

        valido, mensaje = self.verificar_piloto(piloto)
        print(f"  Piloto:       {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        valido, mensaje = self.verificar_aeronave(aeronave)
        print(f"  Aeronave:     {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        valido, mensaje = self.verificar_capacidad(vuelo, aeronave)
        print(f"  Capacidad:    {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        valido, mensaje = self.verificar_clima(clima_favorable)
        print(f"  Clima:        {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        valido, mensaje = self.verificar_pista(pista_libre)
        print(f"  Pista:        {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        valido, mensaje = self.verificar_combustible(combustible_suficiente)
        print(f"  Combustible:  {mensaje}")
        if not valido:
            motivos_rechazo.append(mensaje)

        if len(motivos_rechazo) == 0:
            vuelo.estado = "Autorizado"
            vuelo.piloto = piloto
            vuelo.aeronave = aeronave
            return True, []

        vuelo.estado = "Denegado"
        return False, motivos_rechazo


class ConsultasVuelos:
    def __init__(self, vuelos: list[Vuelo]) -> None:
        self.vuelos = vuelos

    def mostrar_todos(self) -> None:
        print("\nHISTORIAL DE VUELOS")
        if not self.vuelos:
            print("  (ningun vuelo registrado)")
            return
        for i, vuelo in enumerate(self.vuelos, 1):
            print(
                f"  {i}. [{vuelo.estado}] {vuelo.codigo} | "
                f"{vuelo.origen} -> {vuelo.destino} | {vuelo.cantidad_pasajeros} pax"
            )

    def mostrar_autorizados(self) -> None:
        print("\nVUELOS AUTORIZADOS")
        autorizados = [v for v in self.vuelos if v.estado == "Autorizado"]
        if not autorizados:
            print("  (ninguno)")
            return
        for i, vuelo in enumerate(autorizados, 1):
            nombre_piloto = (
                vuelo.piloto.nombre if vuelo.piloto is not None else "Sin asignar"
            )
            modelo_aeronave = (
                vuelo.aeronave.modelo if vuelo.aeronave is not None else "Sin asignar"
            )
            print(f"  {i}. {vuelo.codigo} | {vuelo.origen} -> {vuelo.destino}")
            print(f"     Piloto: {nombre_piloto} | Aeronave: {modelo_aeronave}")
            print(f"     Pasajeros: {vuelo.cantidad_pasajeros}")

    def mostrar_denegados(self) -> None:
        print("\nVUELOS DENEGADOS")
        denegados = [v for v in self.vuelos if v.estado == "Denegado"]
        if not denegados:
            print("  (ninguno)")
            return
        for i, vuelo in enumerate(denegados, 1):
            print(
                f"  {i}. {vuelo.codigo} | "
                f"{vuelo.origen} -> {vuelo.destino} | {vuelo.cantidad_pasajeros} pax"
            )

    def buscar_vuelo(self) -> None:
        codigo = input("Codigo de vuelo a buscar: ").strip().upper()
        for vuelo in self.vuelos:
            if vuelo.codigo.upper() == codigo:
                print("\n-- FICHA DE VUELO --")
                print(f"  Codigo:     {vuelo.codigo}")
                print(f"  Origen:     {vuelo.origen}")
                print(f"  Destino:    {vuelo.destino}")
                print(f"  Pasajeros:  {vuelo.cantidad_pasajeros}")
                print(f"  Estado:     {vuelo.estado}")
                if vuelo.piloto is not None:
                    print(f"  Piloto:     {vuelo.piloto.nombre}")
                    print(f"  Licencia:   {vuelo.piloto.licencia}")
                    print(f"  Horas:      {vuelo.piloto.horas_vuelo}")
                if vuelo.aeronave is not None:
                    print(f"  Aeronave:   {vuelo.aeronave.modelo}")
                    print(f"  Matricula:  {vuelo.aeronave.matricula}")
                    print(f"  Capacidad:  {vuelo.aeronave.capacidad}")
                return
        print("  Vuelo no encontrado.")

    def filtrar_por_destino(self) -> None:
        destino = input("Destino a filtrar: ").strip().lower()
        resultados = [v for v in self.vuelos if v.destino.lower() == destino]
        print(f"\nVUELOS CON DESTINO: {destino.upper()}")
        if not resultados:
            print("  (ninguno)")
            return
        for i, v in enumerate(resultados, 1):
            print(f"  {i}. [{v.estado}] {v.codigo} - {v.cantidad_pasajeros} pax")

    def mostrar_estadisticas(self) -> None:
        total = len(self.vuelos)
        autorizados = len([v for v in self.vuelos if v.estado == "Autorizado"])
        denegados = len([v for v in self.vuelos if v.estado == "Denegado"])
        pendientes = len([v for v in self.vuelos if v.estado == "Pendiente"])
        total_pasajeros = sum(
            v.cantidad_pasajeros for v in self.vuelos if v.estado == "Autorizado"
        )
        destinos = [v.destino for v in self.vuelos if v.estado == "Autorizado"]
        destino_top = Counter(destinos).most_common(1)
        print("\n" + "=" * 45)
        print("  ESTADISTICAS DE VUELOS")
        print("=" * 45)
        print(f"  Total vuelos:       {total}")
        print(f"  Autorizados:        {autorizados}")
        print(f"  Denegados:          {denegados}")
        print(f"  Pendientes:         {pendientes}")
        if total > 0:
            pct = autorizados / total * 100
            print(f"  Tasa autorizacion:  {pct:.1f}%")
        print(f"  Pasajeros en vuelo: {total_pasajeros}")
        if destino_top:
            print(
                f"  Destino popular:    {destino_top[0][0]} ({destino_top[0][1]} vuelos)"
            )
        print("=" * 45)
