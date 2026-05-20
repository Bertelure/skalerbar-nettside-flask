# Min Bedrift - Nettside med Autentisering og Datalagrting

En skalerbar Flask-nettside med brukerautentisering, dynamisk menysystem og fleksibel datalagrting.

## 🚀 Rask start

### 1. Oppsett av mappestruktur

Opprett følgende mappestruktur fra "Ny mappe"-katalogen:

```
Ny mappe/
├── app.py                    # Hovedapplikasjon
├── config.py                 # Konfigurasjonsinnstillinger
├── database.py               # Database og modeller
├── auth.py                   # Autentiseringsruter
├── pages.py                  # Sider og API-ruter
├── requirements.txt          # Python-avhengigheter
├── templates/                # HTML-templates
│   ├── base.html            # Grunntemplate med meny
│   ├── index.html           # Hjemside
│   ├── login.html           # Innloggingside
│   ├── register.html        # Registreringsside
│   ├── dashboard.html       # Bruker-dashboard
│   ├── about.html           # Om bedriften
│   └── contact.html         # Kontaktinfo
├── static/
│   ├── css/
│   │   └── style.css        # Stilark
│   └── js/
│       └── main.js          # JavaScript-bibliotek
└── db/
    └── (database.db blir opprettet automatisk)
```

### 2. Installasjon av avhengigheter

```bash
pip install -r requirements.txt
```

### 3. Start serveren

```bash
python app.py
```

Besøk deretter: **http://localhost:5000**

## 📋 Funksjoner

✅ **Brukerautentisering** - Registrer og logg inn  
✅ **Sikre passord** - Passord hashes med werkzeug.security  
✅ **Datalagrting** - Lagre brukerdata i database  
✅ **Responsiv design** - Fungerer på alle enheter  
✅ **Dynamisk meny** - Lett å legge til nye sider  
✅ **API for datalagrting** - REST-endepunkter for data

## 🔧 Hvordan legge til nye sider

### 1. Legg til meny-item i `config.py`:

```python
MENU_ITEMS = [
    {'name': 'Hjem', 'url': '/', 'icon': '🏠'},
    {'name': 'Om oss', 'url': '/about', 'icon': 'ℹ️'},
    {'name': 'Din nye side', 'url': '/ny-side', 'icon': '📄'},  # NEY!
]
```

### 2. Opprett template (`templates/ny-side.html`):

```html
{% extends "base.html" %}

{% block title %}Din nye side{% endblock %}

{% block content %}
<h2>Innholdet her</h2>
<p>Din HTML her</p>
{% endblock %}
```

### 3. Legg til rute i `pages.py`:

```python
@pages_bp.route('/ny-side')
def ny_side():
    return render_template('ny-side.html')
```

## 💾 Hvordan legge til datalagrting

### Backend (Flask):

Datalagrting er allerede integrert! API-endepunkter:
- `GET /api/data` - Hent all data
- `GET /api/data/<key>` - Hent spesifikk data
- `POST /api/data/<key>` - Lagre/oppdater data
- `DELETE /api/data/<key>` - Slett data

### Frontend (JavaScript):

Bruk `StorageAPI`-objektet fra `main.js`:

```javascript
// Lagre data
await StorageAPI.setData('navn', 'Jon Doe');

// Hent data
const navn = await StorageAPI.getData('navn');

// Hent all data
const allData = await StorageAPI.getData();

// Slett data
await StorageAPI.deleteData('navn');

// Lagre flere nøkler
await StorageAPI.setDataBulk({
    'telefon': '12345678',
    'adresse': 'Storgaten 123'
});
```

## 📊 Datalagrting - Ekstrautvidelser

Hvis du trenger kompleks datalagrting (eks. for spesifikke datatyper eller relasjoner):

1. **Legg til ny tabell i `database.py`:**

```python
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    field_name = db.Column(db.String(200))
    # ... flere kolonner
```

2. **Legg til ruter i `pages.py`:**

```python
@api_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    profile = UserProfile.query.filter_by(user_id=session['user_id']).first()
    return jsonify(profile_to_dict(profile))
```

## 🎨 CSS Tilpasning

Rediger `static/css/style.css`:
- Endrer farger via `:root` CSS-variabler
- Juster layoutet ved hjelp av grid og flexbox
- Responsive breakpoints på 768px

## 🔒 Sikkerhet

- ✅ Passord er hashet med bcrypt (via Werkzeug)
- ✅ Sesjonbasert autentisering
- ✅ HTTPS anbefales i produksjon
- ✅ SQL-injeksjon beskermet med SQLAlchemy ORM

### Produksjonsveiledning:

```python
# I config.py:
SESSION_COOKIE_SECURE = True  # Krever HTTPS
SESSION_COOKIE_HTTPONLY = True  # Beskyttet fra JavaScript
SECRET_KEY = os.environ.get('SECRET_KEY')  # Sett via miljøvariabel
```

## 📝 Lisensiering

Bruk fritt for både personlig og kommersiell bruk.

---

**Spørsmål?** Dokumentasjonen er bygget inn i hver fil!
