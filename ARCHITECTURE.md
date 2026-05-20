# ARKITEKTUR OG DESIGN

## Systemdesign

```
┌─────────────────────────────────────────────────────────┐
│                    Webleser                              │
│  (HTML + CSS + JavaScript + StorageAPI)                  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
                     ↓
┌─────────────────────────────────────────────────────────┐
│                   Flask Server (app.py)                  │
├─────────────────────────────────────────────────────────┤
│  Routes (auth.py, pages.py)                              │
│  ├── /login, /register, /logout                          │
│  ├── /, /about, /contact, /dashboard                    │
│  └── /api/data/* (lagring-API)                          │
├─────────────────────────────────────────────────────────┤
│  Templates Engine (Jinja2)                               │
│  ├── base.html (grunntemplate)                          │
│  ├── auth-templates                                      │
│  ├── page-templates                                      │
│  └── dashboard-template                                  │
├─────────────────────────────────────────────────────────┤
│  Autentisering (werkzeug.security)                       │
│  ├── Password hashing                                    │
│  ├── Session management                                  │
│  └── login_required dekorator                           │
└────────────────┬────────────────────────────────────────┘
                 │ SQL
                 ↓
┌─────────────────────────────────────────────────────────┐
│              SQLite Database                             │
│  ├── users (id, username, email, password_hash,         │
│  │          user_data[JSON], created_at, updated_at)    │
│  └── [Tilpasbare tabeller]                             │
└─────────────────────────────────────────────────────────┘
```

## Filsammenheng

```
app.py (inngang)
├── IMPORTERER config.py (konfigurasjoner)
├── IMPORTERER database.py (database setup)
├── IMPORTERER auth.py (login/logout)
├── IMPORTERER pages.py (sider og API)
└── SETUP
    ├── Mapper (templates/, static/)
    ├── Templates (Jinja2)
    ├── Database (SQLite)
    ├── Blueprints (rute-registrering)
    └── Start Flask-serveren

auth.py
├── BLUEPRINT: auth_bp
├── RUTER:
│   ├── /login (GET/POST)
│   ├── /register (GET/POST)
│   └── /logout (GET)
└── LOGIC: Autentisering, passord-hashing

pages.py
├── BLUEPRINT: pages_bp (sider)
├── BLUEPRINT: api_bp (datalagrting)
├── SIDER:
│   ├── / (index)
│   ├── /about
│   ├── /contact
│   └── /dashboard
└── API-ENDEPUNKTER:
    ├── GET /api/data (hent all data)
    ├── GET /api/data/<key>
    ├── POST /api/data/<key> (lagre)
    ├── DELETE /api/data/<key>
    └── POST /api/data (bulk)

database.py
├── SQLAlchemy setup
├── User-modell
│   ├── id, username, email, password_hash
│   ├── user_data (JSON-lagring)
│   └── Metoder: set_password, check_password, get_data, set_data
└── init_db (initialisering)

config.py
├── Database-konfigurasjoner
├── Session-innstillinger
├── MENU_ITEMS (dynamisk menysystem)
└── Miljø-konfigurasjoner (dev/prod/test)
```

## Datalagrting - Tre nivåer

### Nivå 1: JSON-lagring (Simple)
```
User.user_data = {"nøkkel": "verdi"}
├── Fleksibelt
├── Enkel
├── Innebygd i User-modell
└── API: /api/data/<key>

Eksempel: Brukerpreferanser
```

### Nivå 2: Egne tabeller (Komplekst)
```
CREATE TABLE something (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    field TEXT,
    ...
)
├── Strukturert
├── Relasjonert
├── Validering
└── API: /api/something/*

Eksempel: Blogginnlegg, produkter
```

### Nivå 3: Eksternt API (Advanced)
```
Flask kaller eksternt API
├── Integrering
├── Skalering
└── Microservices

Eksempel: Stripe, SendGrid
```

## Sikkerhet - Lag for lag

```
1. Frontend
   ├── Input-validering (HTML5)
   ├── CSRF-token (hvis aktivert)
   └── HTTPS (produksjon)

2. Backend
   ├── Autentisering (session)
   ├── Autorisasjon (@login_required)
   ├── Validering
   └── SQL-injeksjon-beskyttelse (ORM)

3. Database
   ├── Passord-hashing (bcrypt)
   ├── Autoincrement IDs
   └── Indekser på PK/FK

4. Infrastruktur
   ├── HTTPS
   ├── Secret key
   ├── Miljøvariabler
   └── Firewalls
```

## Skaleringsarkitektur

### Dynamisk menysystem
```python
# config.py
MENU_ITEMS = [
    {'name': 'Hjem', 'url': '/', 'icon': '🏠'},
    {'name': 'Ny side', 'url': '/ny-side', 'icon': '📄'},  # +1 linje
]

# templates/base.html bruker MENU_ITEMS automatisk
{% for item in menu_items %}
    <a href="{{ item.url }}">{{ item.icon }} {{ item.name }}</a>
{% endfor %}

# Resultat: Meny oppdateres automatisk uten kodeendring!
```

### Blueprint-struktur (modulær)
```python
# Hver feature kan være eget blueprint
auth_bp = Blueprint('auth', __name__)
pages_bp = Blueprint('pages', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# app.py registrerer alle
app.register_blueprint(auth_bp)
app.register_blueprint(pages_bp)
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)

# Enkelt å legge til ny blueprint
commerce_bp = Blueprint('commerce', __name__, url_prefix='/shop')
app.register_blueprint(commerce_bp)
```

### Template-hierarki
```
base.html (header, nav, footer, CSS)
├── index.html
├── auth/
│   ├── login.html
│   └── register.html
├── pages/
│   ├── about.html
│   └── contact.html
└── dashboard.html

Enkelt å:
- Tilpasse base.html → alle sider oppdateres
- Legge til ny template-fil
- Bruke {% extends %} for arvinger
```

## Databaseskjema (utviding)

### Eksisterende
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(200),
    user_data TEXT,  -- JSON-lagring
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

INDEX: username, email (rask søk)
```

### Eksempel: Blogg (du kan legge til)
```sql
CREATE TABLE blog_posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY REFERENCES users(id),
    title VARCHAR(200),
    content TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE blog_comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER FOREIGN KEY,
    user_id INTEGER FOREIGN KEY,
    content TEXT,
    created_at TIMESTAMP
);
```

## API-endepunkter

### Autentisering
```
POST   /login             - Logg inn
POST   /register          - Registrer
GET    /logout            - Logg ut
```

### Sider
```
GET    /                  - Hjem
GET    /about             - Om
GET    /contact           - Kontakt
GET    /dashboard         - Dashboard (krever innlogging)
```

### Data-API (krever innlogging)
```
GET    /api/data                    - Hent all brukerdata
GET    /api/data/<key>              - Hent en nøkkel
POST   /api/data/<key>              - Sett/oppdater nøkkel
DELETE /api/data/<key>              - Slett nøkkel
POST   /api/data                    - Sett flere nøkler (bulk)
```

## Deployment-arkitektur

### Development
```
laptop/server$ python app.py
↓
Development-server (Flask)
↓
http://localhost:5000
```

### Production
```
internet
  ↓
Nginx (HTTPS, load balancing)
  ↓
Gunicorn (4 workers)
  ↓
Flask app.py (4 prosesser)
  ↓
PostgreSQL (persistent)
```

## Performance-hensyn

1. **Database**
   - Indekser på username, email
   - JSON-lagring for fleksibilitet
   - Caching mulig via Redis

2. **Frontend**
   - CSS minifisering (produksjon)
   - Lazy loading av images
   - Client-side caching

3. **Backend**
   - Blueprint-struktur (rask)
   - ORM (SQLAlchemy) - sikkerhet over hastighet
   - Mulig: Redis for sessjoner

4. **Skalering**
   - Horisontalt: Flere Gunicorn-prosesser
   - Vertikal: Større server
   - Database: Migrering til PostgreSQL

---

**Arkitektur designet for:**
- 🚀 Rask utvidelse
- 🔒 Sikkerhet fra dag 1
- 📱 Responsive design
- 🔄 Enkle datalagringsløsninger
