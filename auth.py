# Flask Routes for Authentication

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Innloggingsside"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Innlogging vellykket!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Feil brukernavn eller passord', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registreringsside"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Validering
        if not username or not email or not password:
            flash('Alle felt er påkrevd', 'error')
            return render_template('register.html')
        
        if password != password_confirm:
            flash('Passordene stemmer ikke', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Brukernavn finnes allerede', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('E-post finnes allerede', 'error')
            return render_template('register.html')
        
        # Opprett ny bruker
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Bruker opprettet! Logg inn nå.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    """Logg ut bruker"""
    session.clear()
    flash('Du er nå logget ut', 'info')
    return redirect(url_for('main.index'))
