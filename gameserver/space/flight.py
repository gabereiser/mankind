from typing import List, Optional
from dataclasses import dataclass
from uuid import UUID
import models

@dataclass
class Waypoint:
    s: UUID
    x: float
    y: float
    z: float
    
@dataclass
class SolarSystemWaypoint(Waypoint):
    system: models.StarSystem

@dataclass
class OrbitalBodyWaypoint(Waypoint):
    body: models.OrbitalBody

@dataclass
class Departure:
    id: UUID
    s: str
    
@dataclass
class Arrival:
    id: UUID
    s: str

@dataclass
class FlightPlan:
    id: int
    departure: Departure
    arrival: Arrival
    waypoints: List[Waypoint] = []
    current_waypoint: Waypoint

@dataclass
class Formation:
    leader: UUID
    
class FlightController:
	flight_plan: Optional[FlightPlan] = None
	formation: Optional[Formation] = None
