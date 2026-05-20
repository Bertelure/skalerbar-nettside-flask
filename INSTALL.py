#!/usr/bin/env python3
"""
INSTALLASJONS- OG STARTGUIDE
=============================

Denne filen inneholder instruksjoner for å kjøre nettsiden.

STEG 1: Installe Python-avhengigheter
--------------------------------------
Åpne kommandolinja og kjør:

    pip install -r requirements.txt

STEG 2: Opprett mappestruktur
------------------------------
Opprett disse mappene i samme mappe som app.py:

    templates/           (HTML-filer)
    templates/components/
    static/              (CSS og JS)
    static/css/
    static/js/
    db/                  (Database-fil)

Alternativt: Kjør bare app.py og applikasjonen vil opprette mappene automatisk!

STEG 3: Flytt filer til riktig sted
------------------------------------
Flytt disse filene:

    base.html, index.html, login.html, register.html, 
    dashboard.html, about.html, contact.html  →  templates/

    style.css  →  static/css/
    main.js    →  static/js/

STEG 4: Start serveren
---------------------
Kjør:

    python app.py

STEG 5: Besøk nettsiden
-----------------------
Åpne nettleser og gå til:

    http://localhost:5000

Du burde nå se hjemmesiden med funksjonell autentisering!

FEILSØKING
==========

Problem: "ModuleNotFoundError: No module named 'flask'"
Løsning: Kjør 'pip install -r requirements.txt'

Problem: "TemplateNotFound"
Løsning: Sjekk at HTML-filene er i 'templates/' mappen

Problem: Port 5000 er allerede i bruk
Løsning: Rediger i app.py: app.run(debug=True, port=5001)

Problem: Database-feil
Løsning: Slett 'db/database.db' og kjør app.py på nytt

VIDEREUTVIKLINGSRESSURSER
=========================

1. Dokumentasjon i README.md
2. Kodekompmentarer i hver fil
3. Flask offisiell dokumentasjon: https://flask.palletsprojects.com/

KONTAKT
=======
Spørsmål eller problemer? Se dokumentasjonen i hver Python-fil.
"""

if __name__ == '__main__':
    print(__doc__)
    input("\nTrykk Enter for å lukke...")
