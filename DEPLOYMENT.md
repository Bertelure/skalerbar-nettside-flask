# DEPLOYMENT GUIDE - PythonAnywhere

## 📋 Oversikt

Dette dokumentet viser hvordan du deployer den skalerbare nettsiden til PythonAnywhere som testmiljø.

**Miljødetaljert:**
- Platform: PythonAnywhere (Paid account)
- URL: https://vetlesteinstad.pythonanywhere.com
- Python versjon: 3.9+
- Database: SQLite (testdata)

---

## 🔧 STEG 1: Forberedelse

### 1.1 Sjekk at alt er committed til GitHub

```bash
git status
git add .
git commit -m "Deploy: Prepare for PythonAnywhere"
git push origin main
```

### 1.2 Opprett .gitignore (hvis ikke eksisterer)

```
__pycache__/
*.pyc
*.pyo
.env
db/*.db
instance/
.DS_Store
```

### 1.3 Opprett produksjonskonfigurasjoner

Lag `config.production.py`:

```python
import os

class ProductionConfig:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PREFERRED_URL_SCHEME = 'https'
```

---

## 🚀 STEG 2: PythonAnywhere Setup

### 2.1 Logg inn på PythonAnywhere

1. Gå til https://www.pythonanywhere.com/
2. Logg inn med: vetlesteinstad@gmail.com
3. Gå til Dashboard

### 2.2 Opprett Web App

1. Klikk "Web" i toppmeny
2. Klikk "Add a new web app"
3. Velg "Manual configuration"
4. Velg Python 3.9
5. Klikk "Next"

**Resultat:** WSGI-fil og domene er opprettet

---

## 💾 STEG 3: Klon Repository

### 3.1 Åpne Bash Console

1. I PythonAnywhere Dashboard: "Consoles" → "Bash"
2. Kjør kommandoer under:

### 3.2 Klon fra GitHub

```bash
cd ~
git clone https://github.com/Bertelure/skalerbar-nettside-flask.git
cd skalerbar-nettside-flask
ls -la
```

**Resultat:** Prosjektet er lastet ned

---

## 🐍 STEG 4: Virtual Environment

### 4.1 Opprett Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.9 venv
```

### 4.2 Aktiver Virtual Environment

```bash
workon venv
```

### 4.3 Installer Avhengigheter

```bash
pip install -r requirements.txt
```

**Output skal vise:**
```
Successfully installed Flask-2.3.3 Flask-SQLAlchemy-3.0.5 ...
```

---

## 📝 STEG 5: WSGI-fil Konfigurasjons

### 5.1 Rediger WSGI-filen

I PythonAnywhere Web:
1. Klikk på "Web" → ditt webapp-navn
2. Klikk på WSGI-fil-linken
3. Rediger innholdet:

```python
import sys
import os

# Legg til prosjektmappen til path
project_folder = '/home/vetlesteinstad/skalerbar-nettside-flask'
sys.path.insert(0, project_folder)

# Aktiver virtual environment
activate_this = '/home/vetlesteinstad/.virtualenvs/venv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Import Flask-app
from app import create_app

# Opprett app
app = create_app('development')  # Use 'production' later

# Kjør applikasjonen
if __name__ == '__main__':
    app.run()
```

### 5.2 Lagre WSGI-filen

Klikk "Save" i toppmeny

---

## 🔑 STEG 6: Miljøvariabler

### 6.1 Sett Environment Variables

I Bash Console:

```bash
# Rediger ~/.bashrc
nano ~/.bashrc

# Legg til på slutten:
export SECRET_KEY='dev-secret-key-change-later'
export FLASK_ENV='development'

# Lagre (Ctrl+X, Y, Enter)
source ~/.bashrc
```

### 6.2 Verifiser

```bash
echo $SECRET_KEY
# Skal skrive ut: dev-secret-key-change-later
```

---

## 📊 STEG 7: Database Setup

### 7.1 Initaliserer Database

I Bash Console:

```bash
cd ~/skalerbar-nettside-flask
workon venv
python

# I Python REPL:
from app import create_app
app = create_app()
with app.app_context():
    from database import db
    db.create_all()
    print("Database created!")

exit()
```

### 7.2 Opprett Test-brukere

```bash
python

# I Python REPL:
from app import create_app
from database import db, User

app = create_app()
with app.app_context():
    # Opprett test-brukere
    test_users = [
        {'username': 'audun', 'email': 'audun@test.no'},
        {'username': 'seba', 'email': 'seba@test.no'},
        {'username': 'marius', 'email': 'marius@test.no'},
        {'username': 'ingrid', 'email': 'ingrid@test.no'},
        {'username': 'lars', 'email': 'lars@test.no'},
    ]
    
    for user_data in test_users:
        user = User(
            username=user_data['username'],
            email=user_data['email']
        )
        user.set_password(user_data['username'] + '123')
        db.session.add(user)
    
    db.session.commit()
    print("Test users created!")
    
    # Verifiser
    for user in User.query.all():
        print(f"- {user.username} (created: {user.created_at})")

exit()
```

**Test-brukere opprettet:**
- audun / audun123
- seba / seba123
- marius / marius123
- ingrid / ingrid123
- lars / lars123

---

## ✅ STEG 8: Aktivering & Testing

### 8.1 Reload Web App

I PythonAnywhere Dashboard:
1. Gå til "Web"
2. Klikk grønn "Reload"-knapp
3. Vent 1-2 minutter

### 8.2 Test Applikasjonen

Åpne: https://vetlesteinstad.pythonanywhere.com

**Du burde se:**
- ✅ Hjemmeside lastet
- ✅ Menyen vises
- ✅ Login-knapp tilgjengelig

### 8.3 Test Innlogging

1. Klikk "Logg inn"
2. Bruk: `audun` / `audun123`
3. Du burde se Dashboard

---

## 🔐 Sikkerhet Sjekkliste

- [ ] SECRET_KEY endret fra default
- [ ] HTTPS aktivert (standard på PythonAnywhere)
- [ ] SESSION_COOKIE_SECURE = True i produksjon
- [ ] Databasefil er sikret (ikkje public)
- [ ] Error pages ikke viser sensitiv info

---

## 📈 Monitoring & Logging

### Logs på PythonAnywhere

```bash
# Web app error log
cat /var/log/vetlesteinstad.pythonanywhere.com.error.log

# Web app access log
cat /var/log/vetlesteinstad.pythonanywhere.com.access.log

# Server log (tail -f for real-time)
tail -f /var/log/pythonanywhere.error.log
```

### Debugging

Hvis app ikke laster:
1. Sjekk error logs
2. Klikk "Reload" igjen
3. Verifiser Virtual Environment
4. Sjekk WSGI-fil

---

## 🔄 Oppdateringer & Deployment

### Deployer ny versjon

```bash
cd ~/skalerbar-nettside-flask
git pull origin main
workon venv
pip install -r requirements.txt

# I PythonAnywhere Web: Klikk "Reload"
```

### Rollback

```bash
cd ~/skalerbar-nettside-flask
git revert HEAD
git push origin main

# I PythonAnywhere Web: Klikk "Reload"
```

---

## 📊 Produksjon (Senere)

Når applikasjonen er klar for produksjon:

1. **Database:** Migrate til PostgreSQL
2. **SSL:** Bruk custom domain med SSL
3. **Backups:** Enable automated backups
4. **Monitoring:** Sett opp error tracking
5. **Config:** Bruk production-config

---

## 🆘 Feilsøking

| Problem | Løsning |
|---------|---------|
| `ModuleNotFoundError: flask` | Sjekk at virtual environment er aktivt (`workon venv`) |
| `TemplateNotFound` | Sjekk at templates/ mappen er korrekt |
| Endringer vises ikke | Klikk "Reload" i PythonAnywhere Web |
| Database error | Kjør `db.create_all()` på nytt |
| 502 Bad Gateway | Sjekk error log, klikk "Reload" |

---

## 📞 Support

- PythonAnywhere Help: https://help.pythonanywhere.com/
- GitHub Issues: https://github.com/Bertelure/skalerbar-nettside-flask/issues
- Flask Docs: https://flask.palletsprojects.com/

---

## ✨ Gratulerer!

Applikasjonen er nå live på:
### **https://vetlesteinstad.pythonanywhere.com**

Test-konto: `audun` / `audun123`

---

**Versjon:** 1.0.0  
**Sist oppdatert:** 2026-05-20
