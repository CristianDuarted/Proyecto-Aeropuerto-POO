# Proyecto Aeropuerto — Sistema de Pasajeros y Torre de Control

Sistema que simula el control de pasajeros y de vuelos en un aeropuerto,
desarrollado en Python 3 aplicando Programación Orientada a Objetos:
encapsulamiento, validación de datos, manejo de excepciones y separación en
paquetes por responsabilidad.

---

## Arquitectura y Estructura del Proyecto

El proyecto está organizado como un paquete (`Proyecto_aeropuerto/`) con un
script de entrada principal (`run.py`):

```text
Proyecto-Aeropuerto-POO/
├── Proyecto_aeropuerto/
│   ├── main.py                     # Arranca el programa y maneja el menú
│   ├── Consola.py                  # Funciones para leer y validar datos del usuario
│   ├── Aeropuerto.py                # Pasajero, Documento, Equipaje, ValidadorPasajero
│   ├── torre_control.py             # Piloto, Aeronave, Vuelo, ControladorAereo
│   ├── Sistemas/
│   │   ├── sistema_aeropuerto.py    # Registro de pasajeros de principio a fin
│   │   └── sistema_torre_control.py # Registro de vuelos y cola de prioridad
│   ├── consultas/
│   │   ├── sistema_consultas.py     # Búsquedas, filtros y reportes de pasajeros
│   │   └── consultas_vuelos.py      # Búsquedas, filtros y reportes de vuelos
│   └── reportes/                    # Reportes .txt generados al ejecutar el programa
├── run.py                           # Archivo que se ejecuta para iniciar el sistema
├── requirements.txt
└── README.md
```

### Diagrama de clases



## Tecnologías y Conceptos Aplicados

- **Lenguaje:** Python 3.10+
- **Encapsulamiento:** Cada clase agrupa solo los datos y métodos que le
  corresponden (por ejemplo, `Pasajero` no sabe nada de vuelos, y `Vuelo` no
  sabe nada de equipaje).
- **Separación de responsabilidades:** El proyecto se dividió en paquetes
  según lo que hace cada parte (modelos de datos, validación de reglas,
  sistemas que orquestan el flujo, consultas y reportes).
- **Cola de prioridad:** Se usa `queue.PriorityQueue` para que los vuelos
  con mayor urgencia (emergencia, urgente) se procesen antes que los
  vuelos normales, sin importar el orden en que se registraron.
- **Manejo de excepciones:** Se capturan errores al momento de guardar los
  reportes en archivo (`OSError`), y se valida todo lo que escribe el
  usuario por consola (números, texto, sí/no) para que el programa no se
  caiga si alguien escribe algo inválido.
- **Reutilización de código:** La clase `Consola` centraliza las funciones
  de lectura de datos para no repetir el mismo código de validación en
  cada parte del sistema.

---

## Instalación y Ejecución

No se necesitan librerías externas obligatorias, solo tener Python
instalado.

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/dabarretor/Proyecto-Aeropuerto-POO.git
   cd Proyecto-Aeropuerto-POO
   ```

2. **Crear un entorno virtual** (para instalar dependencias sin afectar el
   resto de tu computador):
   ```bash
   python3 -m venv venv
   ```

3. **Activarlo:**
   - Linux / macOS:
     ```bash
     source venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     venv\Scripts\Activate.ps1
     ```

4. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar el programa:**
   ```bash
   python run.py
   ```

## Casos de Uso Demostrados

Al correr el programa, se pueden probar los siguientes flujos:

1. **Registro y validación de pasajeros:** se piden los datos del
   pasajero, su documento y su equipaje, y el sistema decide si queda
   aprobado o rechazado según si cumple los requisitos (pasaporte vigente,
   visa si la necesita, check-in y boleto válido).
2. **Cobro por exceso de equipaje:** si el pasajero se pasa de maletas,
   peso o dimensiones, su equipaje se manda a bodega y se le calcula un
   cargo adicional.
3. **Registro de vuelos con prioridad:** se registran uno o varios vuelos
   con su piloto, aeronave y condiciones de despegue, indicando qué tan
   urgente es cada uno (1 = emergencia, 5 = normal). El sistema los
   procesa en ese orden, sin importar en qué orden se registraron.
4. **Autorización o denegación de despegue:** cada vuelo se revisa contra
   varios requisitos (horas de vuelo del piloto, disponibilidad de la
   aeronave, capacidad de pasajeros, clima, pista y combustible). Si
   alguno falla, el vuelo queda denegado y se muestra el motivo.
5. **Consultas y filtros:** desde el menú se pueden buscar pasajeros o
   vuelos por nombre/código, filtrar por destino, nacionalidad o rango de
   edad, y ver estadísticas generales (tasa de aprobación, destino más
   frecuente, dinero recaudado, etc.).
6. **Exportación de reportes:** se puede generar un archivo `.txt` con el
   resumen final de pasajeros aprobados/rechazados y otro con el resumen
   de vuelos autorizados/denegados, guardados en `reportes/`.


