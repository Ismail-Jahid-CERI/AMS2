from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
from datetime import datetime

class ActionCoursDuJour(Action):
    def name(self):
        return "action_cours_du_jour"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        today = datetime.now().date().isoformat()

        # Connexion à la base SQLite
        conn = sqlite3.connect("edt.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date_debut, date_fin, resume, salle
            FROM cours
            WHERE date(date_debut) = ?
            ORDER BY date_debut ASC
        """, (today,))
        results = cursor.fetchall()
        conn.close()

        # Construction du message
        if not results:
            dispatcher.utter_message("📭 Tu n'as pas cours aujourd'hui !")
        else:
            message = "📘 Voici tes cours aujourd'hui :\n"
            for start, end, title, salle in results:
                heure_debut = datetime.fromisoformat(start).strftime("%H:%M")
                heure_fin = datetime.fromisoformat(end).strftime("%H:%M")
                message += f"- {title} de {heure_debut} à {heure_fin} en {salle}\n"

            dispatcher.utter_message(message)

        return []
