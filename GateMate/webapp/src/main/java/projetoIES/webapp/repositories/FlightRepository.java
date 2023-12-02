package projetoIES.webapp.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;

import projetoIES.webapp.entities.Flight;

public interface FlightRepository extends MongoRepository<Flight, Integer> {
    public Flight findByFlight_iata(String flight_iata);
}
