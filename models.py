from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from typing import Optional

class FlightCategory(str, Enum):
    Black = "Black"
    Platinum = "Platinum"
    Gold = "Gold"
    Normal = "Normal"

class Passenger(BaseModel):
    id: int
    name: str
    hasConnections: bool
    age: int
    flightCategory: FlightCategory = FlightCategory.Normal
    reservationId: str
    hasCheckedBaggage: bool

class Flight(BaseModel):
    flightCode: str
    capacity: int
    passengers: List[Passenger]

class FlightCodeUpdate(BaseModel):
    newFlightCode: str

class PassengerUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    hasConnections: Optional[bool] = None
    age: Optional[int] = None
    flightCategory: Optional[FlightCategory] = None
    hasCheckedBaggage: Optional[bool] = None
