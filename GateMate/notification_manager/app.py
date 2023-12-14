import socket
import logging
import threading
import json

import time
import os
from pymongo import MongoClient
import smtplib


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sent_email(data, collection, servidor_email, remetente):
    data = data.decode()
    json_data = json.loads(data)

    doc = collection.find_one({"flightIata": json_data["flightIata"]})
    if doc is None:
        logger.info("No document found")
        return

    message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\
    %s
    """ % (
        remetente,
        ", ".join(doc["users"]),
        "Flight Updates",
        json.dumps(json_data),
    )
    # Não funciona, pois otlook marca mail como spam
    # servidor_email.sendmail(remetente, doc["users"], message)
    print("Email sent")


def start_server(collection):
    PORT = 1234
    ADDRESS = "0.0.0.0"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ADDRESS, PORT))
    s.listen(5)

    logging.info(f"Server listening on {ADDRESS}:{PORT}")

    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        sent_email(data, collection, servidor_email, remetente)
        conn.close()


if __name__ == "__main__":
    mongo_client = MongoClientmongo_client = MongoClient(f"mongodb://mongodb:27017/")
    db = mongo_client["my_mongodb_database"]
    if "subscribed_flights" not in db.list_collection_names():
        db.create_collection("subscribed_flights")
    collection = db["subscribed_flights"]

    servidor_email = smtplib.SMTP("smtp-mail.outlook.com", 587)
    servidor_email.starttls()
    logger.info(servidor_email)

    servidor_email.login("gatemate4.2023@outlook.pt", "GateMate4_2023.")

    remetente = "gatemate4.2023@outlook.pt"

    threading.Thread(target=start_server(collection)).start()
