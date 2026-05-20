# UTVIDELSESVEILEDNING - Skalerbar Nettside

Denne veiledningen viser hvordan du enkelt kan utvide nettsiden med nye sider og lagringsfunksjoner.

## 📌 Arkitekturoverview

```
Bruker → Templates (HTML) → App.py (Flask)
                              ↓
                        Routes (auth.py, pages.py)
                              ↓
                        Database (database.py)
```

---

## 🆕 Legge til ny side

### Eksempel: Legg til "Blogg"-siden

#### STEG 1: Oppdater menyen i `config.py`

```python
MENU_ITEMS = [
    {'name': 'Hjem', 'url': '/', 'icon': '🏠'},
    {'name': 'Om oss', 'url': '/about', 'icon': 'ℹ️'},
    {'name': 'Kontakt', 'url': '/contact', 'icon': '📧'},
    {'name': 'Blogg', 'url': '/blog', 'icon': '📝'},  # NY SIDE
]
```

#### STEG 2: Opprett HTML-template `templates/blog.html`

```html
{% extends "base.html" %}

{% block title %}Blogg - Min Bedrift{% endblock %}

{% block content %}
<section class="blog">
    <h2>Blogg</h2>
    <p>Siste innlegg og nyheter</p>
    
    <div class="blog-posts">
        <article class="blog-post">
            <h3>Første innlegg</h3>
            <p>Innholdet her...</p>
        </article>
    </div>
</section>
{% endblock %}
```

#### STEG 3: Legg til rute i `pages.py`

```python
@pages_bp.route('/blog')
def blog():
    """Blogg-side"""
    return render_template('blog.html')
```

**FERDIG!** Menyitem vises automatisk og siden er tilgjengelig på `/blog`

---

## 💾 Legge til lagringsfunksjoner

### Eksempel 1: Enkel lagring (allerede integrert!)

I dashboarden kan du allerede lagre data via dette JavaScript-kallet:

```javascript
// Lagre brukerdata
await StorageAPI.setData('favorittfarge', 'blå');

// Hent data
const farge = await StorageAPI.getData('favorittfarge');
console.log(farge);  // Skriver ut: "blå"

// Slett data
await StorageAPI.deleteData('favorittfarge');
```

**Bruk tilfeller:**
- Brukerpreferanser
- Innstillinger
- Korte tekster og tall
- Valg brukeren gjør

### Eksempel 2: Kompleks lagring (egne tabeller)

Hvis du trenger lagring med relasjoner eller validering:

#### Opprett ny modell i `database.py`

```python
class BlogPost(db.Model):
    """Modell for blogginnlegg"""
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Tilknytning til bruker
    author = db.relationship('User', backref='blog_posts')
```

#### Opprett API-ruter i `pages.py`

```python
@api_bp.route('/blog-posts', methods=['GET'])
@login_required
def get_blog_posts():
    """Hent alle innlegg for bruker"""
    posts = BlogPost.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'content': p.content,
        'created_at': p.created_at.isoformat()
    } for p in posts])

@api_bp.route('/blog-posts', methods=['POST'])
@login_required
def create_blog_post():
    """Opprett nytt innlegg"""
    data = request.get_json()
    
    post = BlogPost(
        user_id=session['user_id'],
        title=data['title'],
        content=data['content']
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify({'success': True, 'id': post.id}), 201
```

#### Bruk fra frontend

```javascript
// Opprett innlegg
await fetch('/api/blog-posts', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        title: 'Mitt første innlegg',
        content: 'Innholdet her...'
    })
});

// Hent innlegg
const posts = await fetch('/api/blog-posts').then(r => r.json());
```

---

## 🔐 Legge til autentisering på sider

### Beskytt en side (krever innlogging)

I `pages.py`, importer `login_required`:

```python
from functools import wraps
from flask import redirect, url_for

def login_required_page(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@pages_bp.route('/privat')
@login_required_page
def privat_side():
    """Bare innlogget brukere kan se denne"""
    return render_template('privat.html')
```

---

## 🎨 Tilpass design

### Farger endres i `static/css/style.css`

```css
:root {
    --primary-color: #007bff;      /* Blå */
    --secondary-color: #6c757d;    /* Grå */
    --success-color: #28a745;      /* Grønn */
    --danger-color: #dc3545;       /* Rød */
}
```

### Legge til CSS for ny komponent

```css
.blog-posts {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}

.blog-post {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

---

## 📦 Mappestruktur for større prosjekter

Når prosjektet vokser, reorganiser slik:

```
websiteproject/
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── routes/                  # Splittes opp senere
│   ├── __init__.py
│   ├── auth.py
│   ├── pages.py
│   ├── api.py              # API-ruter
│   └── admin.py            # Admin-ruter
├── templates/
│   ├── base.html
│   ├── public/             # Offentlige sider
│   ├── auth/               # Auth-sider
│   └── admin/              # Admin-sider
├── static/
│   ├── css/
│   │   ├── base.css
│   │   └── components.css
│   └── js/
│       ├── main.js
│       └── api.js
└── db/
```

---

## 🚀 Deployment

### Kjør i produksjon

1. **Installer produksjonserver (Gunicorn):**
   ```bash
   pip install gunicorn
   ```

2. **Kjør med Gunicorn:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:create_app()
   ```

3. **Sett opp HTTPS med Nginx/Apache:**
   - Konfigurer SSL-sertifikat
   - Proxy requests til Gunicorn

---

## ✅ Sjekkliste for ny side

- [ ] Legg til meny-item i `config.py`
- [ ] Opprett HTML-template
- [ ] Legg til @app.route i `pages.py`
- [ ] Test siden i nettleser
- [ ] Legg til CSS om nødvendig
- [ ] Test responsivt design (mobil)

---

## 🆘 Feilsøking

| Problem | Løsning |
|---------|--------|
| Menyitem vises ikke | Sjekk `config.py` MENU_ITEMS |
| 404 error | Sjekk at route i `pages.py` matcher URL |
| Template ikke funnet | Sjekk at HTML er i `templates/` |
| CSS virker ikke | Sjekk at filsti i `<link>` er riktig |
| API returnerer 401 | Sjekk at bruker er innlogget |

---

**Lykke til med utvidelsen! 🎉**
