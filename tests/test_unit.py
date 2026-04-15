# TU
import pytest
from app.logic import GymManager
from app.models import Adherent, Salle, Sport

def test_adherent_balance_validation():
    manager = GymManager()
    manager.add_adherent(Adherent(id=1, nom="Test", prenom="User", abonnement="None", solde=10.0))
    manager.add_salle(Salle(id=1, nom="S1", localisation="L1", type_terrain="T1", capacite=5, horaire_ouverture="08:00-20:00"))
    manager.add_sport(Sport(id=1, nom="Yoga", price_ticket=15.0, price_abo=5.0))
    valid, msg = manager.validate_reservation(1, 1, 1, "2026-04-15", "10:00-11:00")
    assert valid is False
    assert msg == "Solde insuffisant"

def test_salle_capacity_validation():
    manager = GymManager()
    manager.add_adherent(Adherent(id=1, nom="Test", prenom="User", abonnement="Premium", solde=100.0))
    manager.add_salle(Salle(id=1, nom="S1", localisation="L1", type_terrain="T1", capacite=1, horaire_ouverture="08:00-20:00"))
    manager.add_sport(Sport(id=1, nom="Yoga", price_ticket=15.0, price_abo=5.0))
    manager.make_reservation(1, 1, 1, "2026-04-15", "10:00-11:00")
    valid, msg = manager.validate_reservation(1, 1, 1, "2026-04-15", "10:00-11:00")
    assert valid is False
    assert msg == "Capacité de la salle atteinte"

def test_opening_hours_validation():
    manager = GymManager()
    manager.add_adherent(Adherent(id=1, nom="Test", prenom="User", abonnement="Premium", solde=100.0))
    manager.add_salle(Salle(id=1, nom="S1", localisation="L1", type_terrain="T1", capacite=5, horaire_ouverture="09:00-18:00"))
    manager.add_sport(Sport(id=1, nom="Yoga", price_ticket=15.0, price_abo=5.0))
    valid, msg = manager.validate_reservation(1, 1, 1, "2026-04-15", "08:00-09:00")
    assert valid is False
    assert msg == "Hors des horaires d'ouverture"
