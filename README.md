# Proyecto de programación orientada a objetos

## Tabla de contenidos

- [Definición_de_alternativa](#definición-de-alternativa)

- [Diagrama_UML](#diagrama-uml)

- [Solución_preliminar](#solución-preliminar)

---

## Definición de alternativa

Un aeropuerto internacional necesita un sistema para administrar el registro de pasajeros, recursos, gastos y ganancias del aereopuerto, para ello, se va a requerir lo siguiente:

1. El sistema debe registrar a los pasajeros y calcular el peso de sus maletas. Si el equipaje excede el límite permitido por la aerolínea, se debe generar un cobro adicional automático.

2. Se debe validar si hay asientos disponibles en el avion. Si hay disponibles, se genera el pase de abordar. Sino, el sistema debe ofrecer una reprogramación automática asignando al pasajero al siguiente vuelo disponible.

3. Revisar y calcular si la gasolina actual del avión es suficiente para llegar al destino.

4. Calcular la rentabilidad de cada despegue. El sistema debe sumar los ingresos y restarle los gastos operativos.

5. Si el vuelo es aprobado para despegar, se debe mostrar en pantalla que fue un exito.

## Diagrama UML

```mermaid
classDiagram

    class Airport {
        +name : String
        +baggage_limit : double
        +extra_baggage : double
        +fuel_cost_per_liter : double
        +register_passenger(passenger : Passenger)
        +validate_available_seats(flight : Flight)
        +assign_passenger_to_flight(passenger : Passenger, flight : Flight)
        +check_fuel(flight : Flight)
        +calculate_profit(takeoff : Takeoff)
        +show_takeoff_success()
    }

    class Passenger {
        +id : String
        +name : String
        +document : String
        +nationality : String
        +calculate_baggage_weight()
        +get_total_baggage_weight()
        +assign_flight(flight : Flight)
    }

    class Baggage {
        +id : String
        +weight : double
        +get_weight()
    }

    class Airline {
        +code : String
        +name : String
        +calculate_extra_charge(extra_weight : double)
    }

    class Flight {
        +flight_number : String
        +origin : String
        +destination : String
        +date_time : DateTime
        +available_seats : int
        +has_available_seats()
        +assign_passenger(passenger : Passenger)
        +calculate_income()
    }

    class Airplane {
        +registration : String
        +seat_capacity : int
        +available_seats : int
        +fuel_capacity : double
        +current_fuel : double
        +fuel_consumption_per_hour : double
        +has_available_seats()
        +has_enough_fuel(hours : double)
        +calculate_required_fuel(hours : double)
    }

    class Takeoff {
        +id : String
        +flight_hours : double
        +income : double
        +operational_costs : double
        +profitability : double
        +calculate_profitability()
    }

    class FlightStatus {
        <<enumeration>>
        SCHEDULED
        APPROVED
        DEPARTED
        CANCELED
    }

    Airport "1" --> "0..*" Passenger : registers
    Passenger "1" --> "0..*" Baggage : owns
    Airport "1" --> "0..*" Flight : manages
    Airport --> Airline : belongs_to
    Flight --> Takeoff : generates
    Airplane --> Takeoff : operates
    Takeoff --> FlightStatus : status
    Flight --> Passenger : assigns
```


## Solución preliminar



- [Volver_al_inicio](#proyecto-de-programación-orientada-a-objetos)
