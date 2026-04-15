from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.models import Adherent, Salle, Sport, Reservation
from app.logic import gym_manager
from typing import List
from contextlib import asynccontextmanager

def init_data():
    gym_manager.add_adherent(Adherent(id=1, nom="Dupont", prenom="Jean", abonnement="None", solde=50.0))
    gym_manager.add_adherent(Adherent(id=2, nom="Martin", prenom="Alice", abonnement="Premium", solde=100.0))
    
    gym_manager.add_salle(Salle(id=1, nom="Salle Cardio", localisation="Niveau 1", type_terrain="Synthetique", capacite=10, horaire_ouverture="08:00-22:00"))
    gym_manager.add_salle(Salle(id=2, nom="Dojo", localisation="Niveau 0", type_terrain="Tatami", capacite=5, horaire_ouverture="09:00-20:00"))
    
    gym_manager.add_sport(Sport(id=1, nom="Yoga", price_ticket=15.0, price_abo=5.0))
    gym_manager.add_sport(Sport(id=2, nom="Crossfit", price_ticket=20.0, price_abo=10.0))

init_data()

app = FastAPI(title="Gym Booking System")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/adherents", response_model=List[Adherent])
def get_adherents():
    return list(gym_manager.adherents.values())

@app.get("/salles", response_model=List[Salle])
def get_salles():
    return list(gym_manager.salles.values())

@app.get("/sports", response_model=List[Sport])
def get_sports():
    return list(gym_manager.sports.values())

@app.get("/reservations", response_model=List[Reservation])
def get_reservations():
    return list(gym_manager.reservations.values())

@app.post("/reservations")
def create_reservation(adherent_id: int, salle_id: int, sport_id: int, date: str, schedule: str):
    try:
        res = gym_manager.make_reservation(adherent_id, salle_id, sport_id, date, schedule)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Gym Booking API is running. Go to /static/index.html"}
