from .modelos import Pasajero, Documento, Equipaje


# Esta clase valida la informacion de un pasajero, sus documentos y su equipaje.
class ValidadorPasajero:
    PAISES_CON_VISA = ["canada", "estados unidos", "australia", "reino unido"]

    def validar_pasajero(
        self,
        pasajero: Pasajero,
        documento: Documento,
        equipaje: Equipaje,
    ) -> tuple[bool, list[str]]:

        motivos_rechazo: list[str] = []

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
            motivos_rechazo.append("No realizo check-in")

        if not documento.boleto_valido:
            motivos_rechazo.append("Boleto invalido")

        if equipaje.armas:
            motivos_rechazo.append("Transporta armas")

        if equipaje.material_inflamable:
            motivos_rechazo.append("Material inflamable")

        if equipaje.elementos_peligrosos:
            motivos_rechazo.append("Elementos peligrosos")

        self.validar_equipaje(equipaje)

        if motivos_rechazo:
            return False, motivos_rechazo

        return True, ["Aprobado"]

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

        for i, maleta in enumerate(equipaje.maletas, 1):
            if maleta["largo"] > 55 or maleta["ancho"] > 40 or maleta["alto"] > 25:
                equipaje.cargo_adicional += 50000.0
                equipaje.en_bodega = True
                print(f"  Maleta {i}: dimensiones exceden el limite, cargo $50.000")


# Esta clase maneja las consultas, filtros y reportes del sistema de aeropuerto.
class SistemaConsultas:
    def __init__(self, aprobados: list, rechazados: list) -> None:
        self.aprobados = aprobados
        self.rechazados = rechazados

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
            print(f"  {i}. {pasajero.nombre} -> {pasajero.destino}{cargo}")

    def mostrar_rechazados(self) -> None:
        print("\nPASAJEROS RECHAZADOS")
        if not self.rechazados:
            print("  (ninguno)")
            return
        for i, (pasajero, motivo) in enumerate(self.rechazados, 1):
            print(f"  {i}. {pasajero.nombre}  |  Motivo: {motivo}")

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
