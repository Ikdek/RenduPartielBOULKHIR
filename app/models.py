from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, time

class Adherent(BaseModel):
    id: int
    nom: str
    prenom: str
    abonnement: str
    solde: float

class Salle(BaseModel):
    id: int
    nom: str
    localisation: str
    type_terrain: str
    capacite: int
    horaire_ouverture: str

class Sport(BaseModel):
    id: int
    nom: str
    price_ticket: float
    price_abo: float

class Reservation(BaseModel):
    id: int
    nom_adherent: str
    date: str
    schedule: str
    salle_id: int
    sport_id: int
