# Esta clase representa a un pasajero y almacena su informacion personal.
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


# Esta clase representa los documentos de un pasajero.
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


# Esta clase representa el equipaje de un pasajero.
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
