import sqlite3
from ics import Calendar
import os

# 🔹 Charger le fichier ICS
fichier_ics = "basic.ics"

if not os.path.exists(fichier_ics):
    print(f"❌ Fichier {fichier_ics} introuvable.")
    exit()

with open(fichier_ics, "r", encoding="utf-8") as f:
    c = Calendar(f.read())

# 🔹 Connexion à la base SQLite
conn = sqlite3.connect("edt.db")
cursor = conn.cursor()

# 🔹 Création de la table
cursor.execute("""
CREATE TABLE IF NOT EXISTS cours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT,
    date_debut TEXT,
    date_fin TEXT,
    resume TEXT,
    salle TEXT,
    description TEXT,
    statut TEXT
)
""")

# 🔹 Insertion des événements
for event in c.events:
    cursor.execute("""
    INSERT INTO cours (uid, date_debut, date_fin, resume, salle, description, statut)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        event.uid,
        event.begin.isoformat(),
        event.end.isoformat(),
        event.name,
        event.location or "",
        event.description or "",
        getattr(event, "status", "inconnu")
    ))

conn.commit()
conn.close()

print("✅ Données importées dans la base edt.db (table: cours)")
