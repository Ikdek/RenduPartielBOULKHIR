document.addEventListener('DOMContentLoaded', () => {
    loadData();
    loadReservations();
    document.getElementById('btn-reserve').addEventListener('click', makeReservation);
});

async function loadData() {
    const [adherents, salles, sports] = await Promise.all([
        fetch('/adherents').then(r => r.json()),
        fetch('/salles').then(r => r.json()),
        fetch('/sports').then(r => r.json())
    ]);

    const adherentSelect = document.getElementById('adherent');
    adherents.forEach(a => {
        const opt = document.createElement('option');
        opt.value = a.id;
        opt.textContent = `${a.prenom} ${a.nom} (${a.solde}€ - ${a.abonnement})`;
        adherentSelect.appendChild(opt);
    });

    const salleSelect = document.getElementById('salle');
    salles.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.id;
        opt.textContent = `${s.nom} (${s.localisation})`;
        salleSelect.appendChild(opt);
    });

    const sportSelect = document.getElementById('sport');
    sports.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.id;
        opt.textContent = s.nom;
        sportSelect.appendChild(opt);
    });
}

async function loadReservations() {
    const reservations = await fetch('/reservations').then(r => r.json());
    const list = document.getElementById('reservations-list');
    list.innerHTML = '';

    reservations.forEach(r => {
        const card = document.createElement('div');
        card.className = 'res-card';
        card.innerHTML = `
            <strong>${r.nom_adherent}</strong>
            <p>📅 ${r.date} à ${r.schedule}</p>
            <p>📍 Salle ID: ${r.salle_id} | Sport ID: ${r.sport_id}</p>
        `;
        list.appendChild(card);
    });
}

async function makeReservation() {
    const adherent_id = document.getElementById('adherent').value;
    const salle_id = document.getElementById('salle').value;
    const sport_id = document.getElementById('sport').value;
    const date = document.getElementById('date').value;
    const schedule = document.getElementById('schedule').value;
    const msg = document.getElementById('status-message');

    try {
        const response = await fetch(`/reservations?adherent_id=${adherent_id}&salle_id=${salle_id}&sport_id=${sport_id}&date=${date}&schedule=${schedule}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (response.ok) {
            msg.textContent = "Réservation réussie !";
            msg.className = "success";
            loadReservations();
            loadData();
        } else {
            msg.textContent = "Erreur: " + data.detail;
            msg.className = "error";
        }
    } catch (err) {
        msg.textContent = "Erreur de connexion au serveur.";
        msg.className = "error";
    }
}
