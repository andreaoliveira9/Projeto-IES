import React, { useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import FlightCard from "../components/FlightCard";
import useFetch from "../hooks/useFetch";
import image1 from "../assets/allflights/1.jpeg";

function AllFlights() {
  /* const { error, isPending, data: flights } = useFetch(""); */

  const flightsData = [
    {
      id: 1,
      origin: "LIS",
      destination: "FRA",
      flightCode: "TP474",
      airline: "TAP Air Portugal",
    },
    {
      id: 2,
      origin: "MAD",
      destination: "US",
      flightCode: "UX1157",
      airline: "Air EUROPA",
    },
  ];

  const [flights, setFlights] = useState(flightsData);
  const [filter, setFilter] = useState({
    flightCode: "",
    from: "",
    to: "",
    company: "",
  });

  // Função para filtrar os voos com base nos filtros selecionados
  const applyFilters = () => {
    const filteredFlights = flightsData.filter((flight) => {
      return (
        flight.flightCode.includes(filter.flightCode) &&
        (filter.from === "" || flight.origin === filter.from) &&
        (filter.to === "" || flight.destination === filter.to) &&
        (filter.company === "" || flight.airline === filter.company)
      );
    });
    setFlights(filteredFlights);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <div>
        <Navbar />
      </div>

      <div className="flex-1">
        <div>
          <img className="h-full w-full object-cover" src={image1} />
        </div>
        <div class="p-20">
          <div class="justify-start items-center inline-flex">
            <div class="text-sky-950 text-5xl font-bold leading-10">
              Find and subscribe flights here
            </div>
          </div>
          <div class="relative mt-5 flex items-center">
            <div className="w-1/5 mr-1">
              <input
                className="pl-2 appearance-none bg-gray-100 text-zinc-600 w-full h-10 text-xl font-normal outline-none inline-flex"
                type="text"
                name="flightCode"
                id="flightCode"
                placeholder=" Code"
                value={filter.flightCode}
                onChange={(e) =>
                  setFilter({ ...filter, flightCode: e.target.value })
                }
              />
            </div>
            <div className="w-1/5 mx-1">
              <select
                class="pl-2 appearance-none bg-gray-100 text-zinc-600 w-full h-10 text-xl font-normal outline-none inline-flex"
                value={filter.from}
                onChange={(e) => setFilter({ ...filter, from: e.target.value })}
              >
                <option value="" selected>
                  From
                </option>
                <option value="LIS">LIS</option>
              </select>
            </div>

            <div className="w-1/5 mx-1">
              <select
                class="pl-2 appearance-none bg-gray-100 text-zinc-600 w-full h-10 text-xl font-normal outline-none inline-fle"
                value={filter.to}
                onChange={(e) => setFilter({ ...filter, to: e.target.value })}
              >
                <option value="" selected>
                  To
                </option>
                <option value="FRA">FRA</option>
              </select>
            </div>
            <div className="w-1/5 mx-1">
              <select
                class="pl-2 appearance-none bg-gray-100 text-zinc-600 w-full h-10 text-xl font-normal outline-none inline-fle"
                value={filter.company}
                onChange={(e) =>
                  setFilter({ ...filter, company: e.target.value })
                }
              >
                <option value="" selected>
                  Company
                </option>
                <option value="TAP Air Portugal">TAP Air Portugal</option>
              </select>
            </div>

            <div class="w-1/5 ml-1">
              <button
                className="w-full bg-blue-700 rounded justify-center items-center inline-flex px-12 py-2 text-center text-white text-base font-bold leading-normal"
                onClick={applyFilters}
              >
                Search
              </button>
            </div>
          </div>
          <div>
            {/* {isPending && <div>Loading...</div>}
            {error && <div>{error}</div>} */}
            {flights &&
              flights.map((flight) => (
                <Link to={`/allflights/${flight.id}`}>
                  <FlightCard flight={flight}></FlightCard>
                </Link>
              ))}
          </div>
        </div>
      </div>

      <div>
        <Footer />
      </div>
    </div>
  );
}

export default AllFlights;
