"""This file creates a small sqlite database consisting of different outputs the chatbot can give based on an emotion.
If the database already exists and is not empty. u don't have to run this file"""

import sqlite3 as sql

conn = sql.connect("ed_outputs.db")

conn.execute(''' CREATE TABLE IF NOT EXISTS outputs
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                output TEXT NOT NULL,
                emotion TEXT NOT NULL,
                score INT NOT NULL
                );
''')

data = [
    ("Laten we de situatie bespreken en een oplossing vinden.", "angry", 0),
    (" Ik begrijp dat je het niet leuk vindt. Ik ge voor jou een oplossing zoeken.", "angry", 0),
    ("Laten we kijken wat er aan de hand is en bekijken hoe we het kunnen oplossen.", "angry", 0),
    ("Laten we kalm blijven en samen naar een bruikbare oplossing zoeken.", "angry", 0),
    ("Als er zaken zijn die moeten worden opgelost, laten we ze uitzoeken  en aanpakken.", "angry", 0),
    ("Fijn om te horen dat je tevreden bent!", "joy", 0),
    ("Het is goed om te horen dat je zo blij bent!", "joy", 0),
    ("Dat is goed nieuws, fijn!", "joy", 0),
    ("Graag gedaan, blij dat ik kan helpen!", "joy", 0),
    ("Wat leuk!", "joy", 0),
    ("Laat me weten hoe ik kan helpen." , "sad", 0),
    ("Als je iets nodig hebt, aarzel dan niet om te vragen.", "sad", 0),
    ("We gaan samen een oplossing zoeken..", "sad", 0),
    ("Als je hulp nodig hebt, laat het me weten.", "sad", 0),
    ("Als er iets is dat je wilt bespreken, sta ik voor je klaar.", "sad", 0),
    ("Kan ik iets doen om je gerust te stellen?", "fear", 0),
    ("Kan ik iets doen tegen je angst?", "fear", 0),
    ("Wees niet Bang, we gaan het oplosssen", "fear", 0),
    ("Is er iets dat je zorgen kan wegnement?", "fear", 0),
    ("Kan iets helpen bij het verminderen van je angst?", "fear", 0),
    ("Ik waardeer je houding.", "love", 0),
    ("Jouw medewerking is fijn.", "love", 0),
    ("Je positieve houding draagt bij aan een prettig gesprek.", "love", 0),
    ("Bedankt voor je inzet en toewijding.", "love", 0),
    ("Je bijdrage wordt gewaardeerd.", "love", 0),



]

conn.executemany("INSERT INTO outputs (output, emotion, score) VALUES(?, ?, ?)", data)
conn.commit()
conn.close()