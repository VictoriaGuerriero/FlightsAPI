from fastapi import FastAPI
from database import get_all_flights_db, create_flight_db, delete_flight_db, get_flight_db, add_passenger_db, delete_all_flights_db, delete_passenger_db, update_flight_code_db, update_passenger_db
from models import Flight, Passenger, PassengerUpdate, FlightCodeUpdate
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FlightsAPI!"}

@app.get("/api/flights")
async def get_flights():
    tasks = await get_all_flights_db()
    return tasks

@app.get("/api/flights/{flight_code}")
async def get_flight(flight_code: str):
    try:
        result = await get_flight_db(flight_code)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/flights")
async def create_flight(flight: Flight):
    try:
        response = await create_flight_db(flight)
        return JSONResponse(content=response, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/flights/{flight_code}")
async def update_flight_code(flight_code: str, updated_data: FlightCodeUpdate):
    try:
        response = await update_flight_code_db(flight_code, updated_data.newFlightCode)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/flights/{flight_code}")
async def delete_flight(flight_code: str):
    try:
        response = await delete_flight_db(flight_code)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/api/flights")
async def delete_all_flights():
    try:
        response = await delete_all_flights_db()
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/api/flights/{flight_code}/passengers")
async def add_passenger(flight_code: str, passenger: Passenger):
    try:
        result = await add_passenger_db(flight_code, passenger)
        return JSONResponse(content=result, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/api/flights/{flight_code}/passengers/{reservation_id}")
async def update_passenger(flight_code: str, reservation_id: str, passenger_update: PassengerUpdate):
    try:
        result = await update_passenger_db(flight_code, reservation_id, passenger_update)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@app.delete("/api/flights/{flight_code}/passengers/{reservation_id}")
async def delete_passenger(flight_code: str, reservation_id: str):
    try:
        result = await delete_passenger_db(flight_code, reservation_id)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))  