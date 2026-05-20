# Flask Routes for Pages and Storage API

from flask import Blueprint, render_template, request, jsonify, session
from functools import wraps
from database import db, User

pages_bp = Blueprint('pages', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

def login_required(f):
    """Dekorator for å sjekke om bruker er innlogget"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@pages_bp.route('/')
def index():
    """Hjemmeside"""
    return render_template('index.html')

@pages_bp.route('/about')
def about():
    """Om bedriften"""
    return render_template('about.html')

@pages_bp.route('/contact')
def contact():
    """Kontaktinfo"""
    return render_template('contact.html')

@pages_bp.route('/dashboard')
def dashboard():
    """Bruker-dashboard (krever innlogging)"""
    if 'user_id' not in session:
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

# API-endepunkter for datalagrting
@api_bp.route('/data', methods=['GET'])
@login_required
def get_data():
    """Hent alle lagret data for bruker"""
    user = User.query.get(session['user_id'])
    return jsonify(user.get_data())

@api_bp.route('/data/<key>', methods=['GET'])
@login_required
def get_data_key(key):
    """Hent spesifikk datakey"""
    user = User.query.get(session['user_id'])
    value = user.get_data(key)
    if value is None:
        return jsonify({'error': 'Key not found'}), 404
    return jsonify({key: value})

@api_bp.route('/data/<key>', methods=['POST'])
@login_required
def set_data_key(key):
    """Sett/oppdater spesifikk datakey"""
    user = User.query.get(session['user_id'])
    data = request.get_json()
    
    if 'value' not in data:
        return jsonify({'error': 'value field required'}), 400
    
    user.set_data(key, data['value'])
    db.session.commit()
    
    return jsonify({'success': True, 'key': key, 'value': data['value']})

@api_bp.route('/data', methods=['POST'])
@login_required
def set_data_bulk():
    """Sett/oppdater flere datanøkler samtidig"""
    user = User.query.get(session['user_id'])
    data = request.get_json()
    
    for key, value in data.items():
        user.set_data(key, value)
    
    db.session.commit()
    return jsonify({'success': True, 'updated': len(data)})

@api_bp.route('/data/<key>', methods=['DELETE'])
@login_required
def delete_data_key(key):
    """Slett spesifikk datakey"""
    user = User.query.get(session['user_id'])
    data = user.get_data()
    
    if key in data:
        del data[key]
        user.user_data = __import__('json').dumps(data)
        db.session.commit()
        return jsonify({'success': True, 'deleted': key})
    
    return jsonify({'error': 'Key not found'}), 404
