from motor.motor_asyncio import AsyncIOMotorClient
import os
from models import Flight, Passenger, PassengerUpdate, FlightCodeUpdate

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["flightsdb"]
collection = db["flights"]

async def get_flight_db(flight_code: str):
    flight = await collection.find_one({"flightCode": flight_code}, {"_id": 0}) #no uso el id porque no esta en la forma de flight
    if not flight:
        raise Exception("Flight not found")
    return flight

async def get_all_flights_db():
    flights = []
    async for flight in collection.find():
        flights.append(Flight(**flight))
    return flights

async def create_flight_db(flight: Flight):
    flight_exist = await collection.find_one({"flightCode": flight.flightCode})
    if flight_exist:
        raise Exception("Flight code already exists")
    
    flight_data = {
        "flightCode": flight.flightCode,
    }

    if flight.passengers:
        flight_data["passengers"] = [
            {
                "id": passenger.id,
                "name": passenger.name,
                "hasConnections": passenger.hasConnections,
                "age": passenger.age,
                "flightCategory": passenger.flightCategory.value,
                "reservationId": passenger.reservationId,
                "hasCheckedBaggage": passenger.hasCheckedBaggage
            } for passenger in flight.passengers
        ]
    else:
        flight_data["passengers"] = []

    result = await collection.insert_one(flight_data)

    if result.acknowledged:
        return {"message": "Flight created", "flightCode": flight.flightCode}
    else:
        raise Exception("Failed to create flight")

async def update_flight_code_db(old_code: str, new_code: str):
    flight = await collection.find_one({"flightCode": old_code})
    if not flight:
        raise Exception("Flight not found")

    code_exists = await collection.find_one({"flightCode": new_code})
    if code_exists:
        raise Exception("New flightCode already exists")

    result = await collection.update_one(
        {"flightCode": old_code},
        {"$set": {"flightCode": new_code}}
    )

    if result.modified_count == 0:
        raise Exception("Failed to update flightCode")

    return {"message": "Flight code updated", "oldCode": old_code, "newCode": new_code}


async def delete_flight_db(flight_code: str):
    result = await collection.delete_one({"flightCode": flight_code})
    if result.deleted_count == 0:
        raise Exception("Flight not found")
    return {"message": "Flight deleted", "flightCode": flight_code}

async def delete_all_flights_db():
    result = await collection.delete_many({})
    if result.deleted_count == 0:
        raise Exception("No flights found to delete")
    return {"message": "All flights deleted", "count": result.deleted_count}

#FUNCIONES PARA PASSENGER
async def add_passenger_db(flight_code: str, passenger: Passenger):
    flight = await collection.find_one({"flightCode": flight_code})
    if not flight:
        raise Exception("Flight not found")
    
    existing = any(p["reservationId"] == passenger.reservationId for p in flight.get("passengers", []))
    if existing:
        raise Exception("Reservation ID already exists")
    
    new_passenger = {
        "id": passenger.id,
        "name": passenger.name,
        "hasConnections": passenger.hasConnections,
        "age": passenger.age,
        "flightCategory": passenger.flightCategory.value,
        "reservationId": passenger.reservationId,
        "hasCheckedBaggage": passenger.hasCheckedBaggage
    }
    
    result = await collection.update_one(
        {"flightCode": flight_code},
        {"$push": {"passengers": new_passenger}}
    )
    
    if result.modified_count == 0:
        raise Exception("Failed to add passenger")
    
    new_passenger_id = str(new_passenger.get("_id", ""))
    return {"message": "Passenger added", "passengerId": new_passenger_id}

async def update_passenger_db(flight_code: str, reservation_id: str, passenger_update: PassengerUpdate):
    updated_data = passenger_update.model_dump(exclude_unset=True)
    if not updated_data:
        raise Exception("No fields to update")

    fields_to_update = {}
    for key, value in updated_data.items():
        fields_to_update[f"passengers.$.{key}"] = value
    
    flight = await collection.find_one({"flightCode": flight_code, "passengers.reservationId": reservation_id})
    if not flight:
        raise Exception("Flight or passenger not found")
    result = await collection.update_one(
        {"flightCode": flight_code, "passengers.reservationId": reservation_id},
        {"$set": fields_to_update}
    )
    if result.modified_count == 0:
        raise Exception("Failed to update passenger or no changes made")
    return {"message": "Passenger updated", "reservationId": reservation_id, "updatedFields": list(fields_to_update.keys())}

async def delete_passenger_db(flight_code: str, reservation_id: str):
    flight = await collection.find_one({"flightCode": flight_code})
    if not flight:
        raise Exception("Flight not found")
    
    result = await collection.update_one(
        {"flightCode": flight_code},
        {"$pull": {"passengers": {"reservationId": reservation_id}}}
    )
    
    if result.modified_count == 0:
        raise Exception("Passenger not found")
    
    return {"message": "Passenger deleted", "reservationId": reservation_id}

