import logging
import asyncio
import json
import pika
from pika.exceptions import ChannelWrongStateError
import datetime
import os
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def db_adaptor_live_data(channel, collection):
    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)

            for flight in data["response"]:
                # logger.info(flight)
                reg_number = flight["reg_number"]
                latitude = float(flight["lat"])
                longitude = float(flight["lng"])
                altitude = float(flight["alt"])
                direction = float(flight["dir"])
                speed = float(flight["speed"])
                vertical_speed = float(flight["v_speed"])
                flight_number = flight["flight_number"]
                flight_iata = flight["flight_iata"]
                departure_icao = flight["dep_icao"]
                departure_iata = flight["dep_iata"]
                arrive_icao = flight["arr_icao"]
                arrive_iata = flight["arr_iata"]
                airline_icao = flight["airline_icao"]
                airline_iata = flight["airline_iata"]

                airline_name = None
                if airline_icao == "QTR":
                    airline_name = "Qatar Airways"
                elif airline_icao == "BAW":
                    airline_name = "British Airways"
                elif airline_icao == "TAP":
                    airline_name = "TAP Air Portugal"
                elif airline_icao == "AFR":
                    airline_name = "Air France"
                elif airline_icao == "AAL":
                    airline_name = "American Airlines"
                elif airline_icao == "FPO":
                    airline_name = "ASL Airlines France"

                existing_flight = collection.find_one({"flightIata": flight_iata})

                data_to_insert = {
                    "flightNumber": flight_number,
                    "airlineIata": airline_iata,
                    "airlineIcao": airline_icao,
                    "airlineName": airline_name,
                    "aircraftRegistration": reg_number,
                    "departure": {
                        "iata": departure_iata,
                        "icao": departure_icao,
                        "terminal": None,
                        "gate": None,
                        "delay": None,
                        "scheduled": None,
                        "estimated": None,
                        "actual": None,
                    },
                    "arrival": {
                        "iata": arrive_iata,
                        "icao": arrive_icao,
                        "terminal": None,
                        "gate": None,
                        "delay": None,
                        "scheduled": None,
                        "estimated": None,
                        "actual": None,
                    },
                    "live_data": {
                        "latitude": latitude,
                        "longitude": longitude,
                        "altitude": altitude,
                        "direction": direction,
                        "speed": speed,
                        "vertical_speed": vertical_speed,
                    },
                }

                if existing_flight is not None:
                    collection.update_one(
                        {"flightIata": flight_iata}, {"$set": data_to_insert}
                    )
                    logger.info("Updated document for flight iata: %s", flight_iata)
                else:
                    data_to_insert["flightIata"] = flight_iata

                    collection.insert_one(data_to_insert)
                    logger.info(
                        "Inserted new document for flight iata: %s", flight_iata
                    )

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    channel.basic_consume(queue="flights", on_message_callback=callback, auto_ack=True)

    logger.info("Waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    mongo_client = MongoClientmongo_client = MongoClient(f"mongodb://mongodb:27017/")
    db = mongo_client["my_mongodb_database"]
    if "flights" not in db.list_collection_names():
        db.create_collection("flights")
    collection = db["flights"]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            "rabbitmq",
            credentials=pika.PlainCredentials(
                os.environ["RABBITMQ_USER"], os.environ["RABBITMQ_PASSWORD"]
            ),
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue="flights")

    asyncio.run(db_adaptor_live_data(channel, collection))
