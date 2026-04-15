from typing import List, Dict, Optional
from app.models import Adherent, Salle, Sport, Reservation
from datetime import datetime

class GymManager:
    def __init__(self):
        self.adherents: Dict[int, Adherent] = {}
        self.salles: Dict[int, Salle] = {}
        self.sports: Dict[int, Sport] = {}
        self.reservations: Dict[int, Reservation] = {}
        self._res_id_counter = 1

    def add_adherent(self, adherent: Adherent):
        self.adherents[adherent.id] = adherent

    def add_salle(self, salle: Salle):
        self.salles[salle.id] = salle

    def add_sport(self, sport: Sport):
        self.sports[sport.id] = sport

    def validate_reservation(self, adherent_id: int, salle_id: int, sport_id: int, date: str, schedule: str) -> bool:
        adherent = self.adherents.get(adherent_id)
        salle = self.salles.get(salle_id)
        sport = self.sports.get(sport_id)

        if not adherent or not salle or not sport:
            return False, "Entité inexistante"

        price = sport.price_ticket if adherent.abonnement == "None" else sport.price_abo
        if adherent.solde < price:
            return False, "Solde insuffisant"

        current_res = [r for r in self.reservations.values() if r.salle_id == salle_id and r.date == date and r.schedule == schedule]
        if len(current_res) >= salle.capacite:
            return False, "Capacité de la salle atteinte"

        open_start, open_end = salle.horaire_ouverture.split('-')
        req_start, req_end = schedule.split('-')
        if req_start < open_start or req_end > open_end:
            return False, "Hors des horaires d'ouverture"

        return True, "OK"

    def make_reservation(self, adherent_id: int, salle_id: int, sport_id: int, date: str, schedule: str):
        valid, msg = self.validate_reservation(adherent_id, salle_id, sport_id, date, schedule)
        if not valid:
            raise ValueError(msg)

        adherent = self.adherents[adherent_id]
        sport = self.sports[sport_id]
        price = sport.price_ticket if adherent.abonnement == "None" else sport.price_abo
        
        adherent.solde -= price
        
        res = Reservation(
            id=self._res_id_counter,
            nom_adherent=f"{adherent.prenom} {adherent.nom}",
            date=date,
            schedule=schedule,
            salle_id=salle_id,
            sport_id=sport_id
        )
        self.reservations[res.id] = res
        self._res_id_counter += 1
        return res

gym_manager = GymManager()
