from Proyecto_aeropuerto.consultas.sistema_consultas import SistemaConsultas
from Proyecto_aeropuerto.consultas.consultas_vuelos import ConsultasVuelos
from Proyecto_aeropuerto.Sistemas.sistema_aeropuerto import SistemaAeropuerto
from Proyecto_aeropuerto.Sistemas.sistema_torre_control import SistemaTorreControl
from Proyecto_aeropuerto.Consola import Consola


class MenuInterfaz:
    def __init__(self, titulo, acciones):
        self.MENU = titulo
        self.ACCIONES = acciones

    def Opcion_menu(self):
        while True:
            print(self.MENU)

            opcion = input("Opción: ").strip()

            if opcion == "0":
                print("\n  Hasta luego.\n")
                break

            accion = self.ACCIONES.get(opcion)

            if accion:
                accion()
            else:
                print("  ✘ Opción no válida.")


def main():

    sistema = SistemaAeropuerto()

    sistema.registrar_pasajero()

    sistema.mostrar_reporte()

    consultas = SistemaConsultas(sistema.aprobados, sistema.rechazados)
    consola = Consola()

    if consola._leer_booleano("¿Deseas registrar vuelos? (s/n): "):
        torre = SistemaTorreControl(sistema.aprobados)

        print("\n" + "=" * 60)
        print("  TORRE DE CONTROL")
        print("=" * 60)
        while True:
            cantidad_vuelos = consola._leer_entero("Cuantos vuelos desea registrar?: ")
            if cantidad_vuelos >= 0:
                break
            print("Error, ingresa un número entero no negativo, por favor")
        for _ in range(cantidad_vuelos):
            torre.registrar_vuelo()

        torre.procesar_cola_despegues()

        consultas_aeropuerto = SistemaConsultas(sistema.aprobados, sistema.rechazados)
        consultas_vuelos = ConsultasVuelos(torre.vuelos)

        MENU = """
        ============================================
                MENU PRINCIPAL
        ============================================
        -- AEROPUERTO --------------------------
        1. Ver pasajeros aprobados
        2. Ver pasajeros rechazados
        3. Buscar pasajero
        4. Filtrar por destino
        5. Filtrar por nacionalidad
        6. Filtrar por rango de edad
        7. Equipaje en bodega
        8. Pasajeros sin cargo
        9. Destinos frecuentes
        10. Estadisticas de pasajeros
        11. Exportar reporte aeropuerto
        -- TORRE DE CONTROL --------------------
        12. Ver todos los vuelos
        13. Ver vuelos autorizados
        14. Ver vuelos denegados
        15. Buscar vuelo por codigo
        16. Filtrar vuelos por destino
        17. Estadisticas de vuelos
        18. Exportar reporte torre
        ----------------------------------------
        0. Salir
        ============================================"""

        ACCIONES = {
            "1": consultas_aeropuerto.mostrar_aprobados,
            "2": consultas_aeropuerto.mostrar_rechazados,
            "3": consultas_aeropuerto.buscar_pasajero,
            "4": consultas_aeropuerto.filtrar_por_destino,
            "5": consultas_aeropuerto.filtrar_por_nacionalidad,
            "6": consultas_aeropuerto.filtrar_por_edad,
            "7": consultas_aeropuerto.mostrar_bodega,
            "8": consultas_aeropuerto.mostrar_sin_cargo,
            "9": consultas_aeropuerto.mostrar_destinos,
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
        menu = MenuInterfaz(MENU, ACCIONES)
        menu.Opcion_menu()
    else:
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
        menu = MenuInterfaz(MENU, ACCIONES)
        menu.Opcion_menu()
