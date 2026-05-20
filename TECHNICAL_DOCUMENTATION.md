# TEKNISK DOKUMENTASJON - Skalerbar Nettside

## 📊 Prosjektinformasjon

| Egenskaper | Verdi |
|-----------|-------|
| **Prosjektnavn** | Skalerbar Nettside med Flask |
| **GitHub Repository** | https://github.com/Bertelure/skalerbar-nettside-flask |
| **GitHub Bruker** | Bertelure |
| **Opprettet** | 2026-05-20 |
| **Status** | Aktiv utvikling |
| **Lisens** | MIT (standard) |

---

## 🔐 Repository Tilgang

### GitHub
- **URL:** https://github.com/Bertelure/skalerbar-nettside-flask
- **Type:** Public
- **Branches:** 
  - `main` - Produksjon
  - `develop` - Utvikling (når opprettet)

### Collaborators
- Primær: Bertelure (vetlesteinstad@gmail.com)

---

## 🚀 Deployment Miljøer

### 1. Development (Lokalt)
```bash
python app.py
# http://localhost:5000
```

### 2. Testing - PythonAnywhere
- **URL:** https://vetlesteinstad.pythonanywhere.com
- **Status:** Aktivt testmiljø
- **Database:** SQLite (testdata)
- **Autoscaling:** Av

**Innloggingsdetaljer (Test Accounts):**

| Brukernavn | Passord | Rolle |
|-----------|---------|-------|
| audun | audun123 | Testbruker |
| seba | seba123 | Testbruker |
| marius | marius123 | Testbruker |
| ingrid | ingrid123 | Testbruker |
| lars | lars123 | Testbruker |

### 3. Production (Fremtidig)
- Planlagt: AWS/Heroku/DigitalOcean
- Database: PostgreSQL
- CDN: CloudFlare
- HTTPS: Let's Encrypt (obligatorisk)

---

## 🏗️ Arkitektur

### Stack
- **Backend:** Flask 2.3.3 + Python 3.9+
- **Database:** SQLite (test) / PostgreSQL (prod)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **ORM:** SQLAlchemy
- **Auth:** Werkzeug Security (bcrypt)

### API Endpoints
```
Authentication:
  POST   /login              - Bruker-innlogging
  POST   /register           - Bruker-registrering
  GET    /logout             - Logg ut

Pages:
  GET    /                   - Hjemside
  GET    /about              - Om bedriften
  GET    /contact            - Kontakt
  GET    /dashboard          - Bruker-dashboard

API (Datalagrting):
  GET    /api/data           - Hent all data
  POST   /api/data/<key>     - Lagre data
  GET    /api/data/<key>     - Hent spesifikk nøkkel
  DELETE /api/data/<key>     - Slett data
```

---

## 📁 Mappestruktur

```
skalerbar-nettside-flask/
├── app.py                    # Flask-applikasjon
├── config.py                 # Konfigurasjoner
├── database.py               # SQLAlchemy modeller
├── auth.py                   # Autentiseringsruter
├── pages.py                  # Sideruter og API
├── requirements.txt          # Python-avhengigheter
├── static/
│   ├── css/style.css        # Responsive CSS
│   └── js/main.js           # StorageAPI
├── templates/
│   ├── base.html            # Grunntemplate
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── about.html
│   └── contact.html
├── db/
│   └── database.db          # SQLite (auto-opprettet)
├── docs/
│   ├── ARCHITECTURE.md      # Systemdesign
│   ├── DEVELOPMENT.md       # Utvidelsesveiledning
│   └── DEPLOYMENT.md        # Deployment-guide (dette dokument)
└── README.md
```

---

## 🔧 Installasjon & Setup

### Lokalt
```bash
# 1. Klon repository
git clone https://github.com/Bertelure/skalerbar-nettside-flask.git
cd skalerbar-nettside-flask

# 2. Installer avhengigheter
pip install -r requirements.txt

# 3. Start serveren
python app.py

# 4. Besøk http://localhost:5000
```

### PythonAnywhere
Se DEPLOYMENT.md for detaljert guide.

---

## 📦 Avhengigheter

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Werkzeug==2.3.7
python-dotenv==1.0.0
```

**Installasjon:**
```bash
pip install -r requirements.txt
```

---

## 🔒 Sikkerhet

### Innebygd
- ✅ Passord-hashing (bcrypt via Werkzeug)
- ✅ SQL-injeksjon-beskyttelse (SQLAlchemy ORM)
- ✅ Session-basert autentisering
- ✅ CSRF-ready (kan aktiveres)

### Best Practices
1. **Environment Variables**
   ```python
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

2. **HTTPS i produksjon**
   - Obligatorisk for alle HTTP-forespørsler
   - SSL-sertifikat fra Let's Encrypt

3. **Database**
   - Backups hver 24 timer
   - Separate dev/test/prod databaser

4. **Access Control**
   - @login_required dekorator på sensitive ruter
   - Rate limiting (implementeres ved behov)

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    user_data TEXT,           -- JSON lagring
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

INDEX: username, email
```

### Struktur for utvidelse
Nye tabeller legges til i `database.py` og migreres med:
```python
db.create_all()
```

---

## 🚀 Deployment Guide

### PythonAnywhere Setup
1. Klon repo fra GitHub
2. Opprett Virtual Environment
3. Installer avhengigheter
4. Sett opp WSGI-fil
5. Konfigurer domene

**Detaljer:** Se DEPLOYMENT.md

---

## 📈 Monitoring & Logging

### PythonAnywhere
- Error Logs: `/var/log/pythonanywhere.error.log`
- Access Logs: `/var/log/pythonanywhere.access.log`
- Web App Console: Tilgjengelig fra dashboard

### Produksjon (Fremtidig)
- Application Insights / New Relic
- Error tracking (Sentry)
- Log aggregation (CloudWatch)

---

## 🔄 CI/CD Pipeline

### GitHub Actions (Anbefalt)
```yaml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

---

## 📝 Versjonering

### Semantic Versioning
- **v1.0.0** - Initial release
- **v1.1.0** - Feature: Blogg-side
- **v2.0.0** - Breaking changes

**Tagging:**
```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

---

## 🤝 Bidrag

### Workflow
1. Lag feature-branch: `git checkout -b feature/ny-funksjon`
2. Commit endringer: `git commit -m "feat: ..."`
3. Push: `git push origin feature/ny-funksjon`
4. Åpne Pull Request på GitHub
5. Merge når godkjent

### Kodestil
- PEP 8 for Python
- 2-space indenting for HTML/CSS/JS
- Docstrings på alle funksjoner

---

## 📞 Support & Kontakt

| Rolle | Kontakt | Ansvar |
|------|---------|--------|
| Developer | vetlesteinstad@gmail.com | App-utvikling |
| DevOps | - | Deployment (fremtidig) |
| Support | - | Brukersti|tte (fremtidig) |

---

## 📚 Ressurser

- Flask-docs: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- PythonAnywhere: https://help.pythonanywhere.com/
- GitHub: https://docs.github.com/

---

## ✅ Sjekkliste for Deploy

- [ ] Repository opprettet på GitHub
- [ ] Alle filer er committed
- [ ] requirements.txt er oppdatert
- [ ] .gitignore er satt
- [ ] DEPLOYMENT.md er lest
- [ ] PythonAnywhere-konto opprettet
- [ ] Virtual Environment satt opp
- [ ] Database initialisert
- [ ] Test-brukere opprettet
- [ ] HTTPS aktivert

---

**Versjon:** 1.0.0  
**Sist oppdatert:** 2026-05-20  
**Opprettet av:** Copilot Assistant
