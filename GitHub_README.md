# 🚀 Skalerbar Nettside med Flask

En moderne, skalerbar nettside bygget med Flask, SQLite og moderne web-teknologi. Inneholder brukerautentisering, datalagrting, responsive design og enkelt å utvide.

**GitHub Repository:** https://github.com/Bertelure/skalerbar-nettside-flask

## ✨ Funksjoner

- ✅ **Brukerautentisering** - Sikker registrering og innlogging
- ✅ **Datalagrting** - Fleksibel JSON-basert lagring
- ✅ **REST API** - Programmatisk tilgang til data
- ✅ **Responsiv Design** - Fungerer på alle enheter
- ✅ **Dynamisk Menysystem** - Lett å legge til nye sider
- ✅ **Skalerbar Arkitektur** - Blueprint-struktur for modulerering
- ✅ **Sikkerhet** - Passord-hashing, SQL-injeksjon-beskyttelse
- ✅ **Dokumentasjon** - Komplett utviklerdokumentation

## 🚀 Quick Start

### Lokalt (Development)

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

### PythonAnywhere (Testing)

Deploy guide: Se [DEPLOYMENT.md](./DEPLOYMENT.md)

Live URL: https://vetlesteinstad.pythonanywhere.com

**Test-konto:**
```
Brukernavn: audun
Passord:    audun123
```

## 📂 Mappestruktur

```
skalerbar-nettside-flask/
├── app.py                    # Flask-applikasjon
├── config.py                 # Konfigurasjoner
├── database.py               # SQLAlchemy modeller
├── auth.py                   # Autentiseringsruter
├── pages.py                  # Sideruter og API
├── requirements.txt          # Python-avhengigheter
├── static/
│   ├── css/style.css        # Responsive design
│   └── js/main.js           # Frontend API
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── about.html
│   └── contact.html
├── db/
│   └── database.db          # SQLite database
└── docs/
    ├── TECHNICAL_DOCUMENTATION.md
    ├── DEPLOYMENT.md
    ├── ARCHITECTURE.md
    └── DEVELOPMENT.md
```

## 🔧 API Endpoints

### Authentication
```
POST   /login              Logg inn bruker
POST   /register           Registrer ny bruker
GET    /logout             Logg ut
```

### Pages
```
GET    /                   Hjemside
GET    /about              Om bedriften
GET    /contact            Kontaktinformasjon
GET    /dashboard          Bruker-dashboard (krever innlogging)
```

### Data Storage API (krever innlogging)
```
GET    /api/data           Hent all brukerdata
POST   /api/data/<key>     Lagre/oppdater data
GET    /api/data/<key>     Hent spesifikk nøkkel
DELETE /api/data/<key>     Slett data
```

## 💾 Database

### User Model
```python
User(
    id=Integer,
    username=String (unique),
    email=String (unique),
    password_hash=String,
    user_data=JSON (fleksibel lagring),
    created_at=DateTime,
    updated_at=DateTime
)
```

### Data Storage
Bruk JSON-kolonen `user_data` for fleksibel lagring:

```javascript
// Lagre data
await StorageAPI.setData('favorittfarge', 'blå');

// Hent data
const farge = await StorageAPI.getData('favorittfarge');

// Hent all data
const allData = await StorageAPI.getData();

// Slett data
await StorageAPI.deleteData('favorittfarge');
```

## 🎨 Tilpassing

### Legge til ny side

1. **Rediger config.py:**
```python
MENU_ITEMS = [
    {'name': 'Min side', 'url': '/min-side', 'icon': '📄'},
]
```

2. **Opprett template `templates/min-side.html`:**
```html
{% extends "base.html" %}
{% block content %}
<h2>Min side</h2>
{% endblock %}
```

3. **Legg til rute i pages.py:**
```python
@pages_bp.route('/min-side')
def min_side():
    return render_template('min-side.html')
```

### Tilpasse design

Rediger `static/css/style.css`:
- Farger: `:root` CSS-variabler
- Layout: Grid og flexbox
- Responsive: Media queries på 768px

Se [DEVELOPMENT.md](./DEVELOPMENT.md) for mer.

## 🔒 Sikkerhet

- Passord hashes med bcrypt (via Werkzeug)
- SQL-injeksjon-beskyttet (SQLAlchemy ORM)
- Session-basert autentisering
- HTTPS i produksjon (obligatorisk)
- CSRF-ready (kan aktiveres)

### Produksjonsforberedelse

```python
# config.py
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECRET_KEY = os.environ.get('SECRET_KEY')  # Fra miljøvariabler
```

## 📚 Dokumentasjon

- [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md) - System og arkitektur
- [DEPLOYMENT.md](./DEPLOYMENT.md) - PythonAnywhere deployment
- [DEVELOPMENT.md](./DEVELOPMENT.md) - Utvidelsesveiledning
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detaljert designbeslutninger

## 🧪 Test-brukere

Opprett test-brukere:

```bash
python setup_test_users.py
```

**Forhåndslaget test-brukere:**
```
audun / audun123
seba / seba123
marius / marius123
ingrid / ingrid123
lars / lars123
```

## 🚀 Production Deployment

### PythonAnywhere (Testing)
Se [DEPLOYMENT.md](./DEPLOYMENT.md) for steg-for-steg guide.

### AWS / Heroku / DigitalOcean (Produksjon)
Planned for future releases.

## 📦 Stack

- **Backend:** Flask 2.3.3
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **ORM:** SQLAlchemy
- **Authentication:** Werkzeug Security

## 🤝 Bidrag

1. Fork repository
2. Lag feature-branch: `git checkout -b feature/min-funksjon`
3. Commit: `git commit -m "feat: beskrivelse"`
4. Push: `git push origin feature/min-funksjon`
5. Åpne Pull Request

## 📝 Lisens

MIT License - Se LICENSE-fil

## 💬 Support

- Issues: https://github.com/Bertelure/skalerbar-nettside-flask/issues
- Dokumentasjon: Se `/docs` mappen
- Flask docs: https://flask.palletsprojects.com/

## ✅ Roadmap

- [x] Grunnstruktur og autentisering
- [x] Datalagrting API
- [x] Responsive design
- [x] PythonAnywhere deployment
- [ ] PostgreSQL support
- [ ] Admin panel
- [ ] Email notifications
- [ ] Rate limiting

---

**Status:** Aktivt under utvikling ✨

**GitHub:** https://github.com/Bertelure/skalerbar-nettside-flask

**Kontakt:** vetlesteinstad@gmail.com
