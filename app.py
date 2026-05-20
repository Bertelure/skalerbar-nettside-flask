from flask import Flask
from config import config, MENU_ITEMS
from database import init_db, db
from auth import auth_bp
from pages import pages_bp, api_bp
import os

def setup_directories():
    """Opprett nødvendige mapper"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    directories = [
        'templates',
        'templates/components',
        'static',
        'static/css',
        'static/js',
        'db',
    ]
    
    for dir_path in directories:
        full_path = os.path.join(base_path, dir_path)
        try:
            os.makedirs(full_path, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create {dir_path}: {e}")
    
    # Ensure db folder exists - critical for database
    db_folder = os.path.join(base_path, 'db')
    if not os.path.exists(db_folder):
        os.makedirs(db_folder, exist_ok=True)

def organize_templates():
    """Organiserer templates fra root til templates-mappen"""
    import shutil
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    template_files = ['base.html', 'index.html', 'login.html', 'register.html', 'dashboard.html', 'about.html', 'contact.html']
    templates_dir = os.path.join(base_path, 'templates')
    
    for fname in template_files:
        src = os.path.join(base_path, fname)
        dst = os.path.join(templates_dir, fname)
        if os.path.exists(src) and not os.path.exists(dst):
            try:
                shutil.move(src, dst)
            except:
                pass

def organize_static():
    """Organiserer CSS og JS fra root til static-mappen"""
    import shutil
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # CSS files
    css_files = ['style.css']
    css_dir = os.path.join(base_path, 'static', 'css')
    for fname in css_files:
        src = os.path.join(base_path, fname)
        dst = os.path.join(css_dir, fname)
        if os.path.exists(src) and not os.path.exists(dst):
            try:
                shutil.move(src, dst)
            except:
                pass
    
    # JS files
    js_files = ['main.js']
    js_dir = os.path.join(base_path, 'static', 'js')
    for fname in js_files:
        src = os.path.join(base_path, fname)
        dst = os.path.join(js_dir, fname)
        if os.path.exists(src) and not os.path.exists(dst):
            try:
                shutil.move(src, dst)
            except:
                pass

def create_app(config_name='development'):
    """Flask app factory"""
    # Opprett mapper først
    setup_directories()
    organize_templates()
    organize_static()
    
    app = Flask(__name__)
    
    # Konfigurasjonsoppsett
    app.config.from_object(config[config_name])
    
    # Database initialisering
    init_db(app)
    
    # Blueprint registrering
    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)
    
    # Gjør menyen tilgjengelig i alle templates
    @app.context_processor
    def inject_menu():
        return dict(menu_items=MENU_ITEMS)
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return '''
        <html>
            <body style="font-family: Arial; text-align: center; padding-top: 50px;">
                <h1>404 - Side ikke funnet</h1>
                <p><a href="/">Tilbake til hjem</a></p>
            </body>
        </html>
        ''', 404
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
