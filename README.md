# ProyectoPOO

# Proyecto de programación orientada a objetos

## Tabla de contenidos

* [Definición de alternativa](#definición-de-alternativa)
* [Diagrama UML](#diagrama-uml)
* [Solución preliminar](#solución-preliminar)

---

# Definición de alternativa

Un aeropuerto internacional necesita un sistema para administrar el registro de pasajeros, recursos, gastos y ganancias del aeropuerto. Para ello, se requiere lo siguiente:

1. El sistema debe registrar a los pasajeros y calcular el peso de sus maletas. Si el equipaje excede el límite permitido por la aerolínea, se debe generar un cobro adicional automático.

2. Se debe validar si hay asientos disponibles en el avión. Si hay disponibles, se genera el pase de abordar. Si no, el sistema debe ofrecer una reprogramación automática asignando al pasajero al siguiente vuelo disponible.

3. Revisar y calcular si la gasolina actual del avión es suficiente para llegar al destino.

4. Calcular la rentabilidad de cada despegue. El sistema debe sumar los ingresos y restarle los gastos operativos.

5. Si el vuelo es aprobado para despegar, se debe mostrar en pantalla que fue un éxito.

---

# Diagrama UML

```mermaid
classDiagram
    class Airport {
        +name : str
        +baggage_limit : float
        +extra_baggage : float
        +fuel_cost_per_liter : float
        +register_passenger(passenger : Passenger)
        +validate_available_seats(flight : Flight)
        +assign_passenger_to_flight(passenger : Passenger, flight : Flight)
        +check_fuel(flight : Flight)
        +calculate_profit(takeoff : Takeoff)
        +show_takeoff_success()
    }

    class Flight {
        +flight_number : str
        +origin : str
        +destination : str
        +date_time : str
        +available_seats : int
        +airplane : Airplane
        +airline : Airline
        +has_available_seats()
        +assign_passenger(passenger : Passenger)
        +calculate_income()
    }

    class Passenger {
        +id : str
        +name : str
        +document : str
        +nationality : str
        +calculate_baggage_weight()
        +get_total_baggage_weight()
        +assign_flight(flight : Flight)
    }

    class Airplane {
        +registration : str
        +seat_capacity : int
        +available_seats : int
        +fuel_capacity : float
        +current_fuel : float
        +fuel_consumption_per_hour : float
        +has_available_seats()
        +has_enough_fuel(hours : float)
        +calculate_required_fuel(hours : float)
    }

    class Airline {
        +code : str
        +name : str
        +calculate_extra_charge(extra_weight : float)
    }

    class Takeoff {
        +id : str
        +flight_hours : float
        +income : float
        +operational_costs : float
        +profitability : float
        +calculate_profitability()
    }

    class Baggage {
        +id : str
        +weight : float
        +get_weight()
    }

    class BoardingPass {
        +code : str
        +seat_number : str
        +boarding_time : str
        +show_information()
    }
    
    class FlightStatus {
        SCHEDULED
        APPROVED
        DEPARTED
        CANCELED
    }

    Airport o-- Flight
    Airport o-- Passenger
    Airport --> Airline
    Flight --> Airplane
    Flight --> Airline
    Flight --> Passenger
    Flight *-- Takeoff
    Passenger *-- Baggage
    Passenger o-- BoardingPass
    Airplane --> Takeoff
    Takeoff --> FlightStatus
```

---

# Solución preliminar

```text
==============================
        AIRPORT SYSTEM
==============================

Passenger registered successfully

Passenger : Andres Perez
Document  : CC 123456

Checking baggage weight...
Total baggage weight : 32 kg
Extra baggage charge : $40

Checking available seats...
Seat assigned : 14A

Generating boarding pass...

==============================
        BOARDING PASS
==============================

Passenger : Andres Perez
Flight    : AV203
Origin    : Bogotá
Destination : Madrid
Seat      : 14A

Checking airplane fuel...
Fuel status : OK

Calculating flight profitability...
Flight profitability : $185000

FLIGHT DEPARTED SUCCESSFULLY
==============================
