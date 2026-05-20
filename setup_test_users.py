#!/usr/bin/env python3
"""
Opprett test-brukere i databasen

Bruk:
    python setup_test_users.py

Test-brukere:
    audun / audun123
    seba / seba123
    marius / marius123
    ingrid / ingrid123
    lars / lars123
"""

from app import create_app
from database import db, User

def setup_test_users():
    """Opprett test-brukere"""
    
    app = create_app()
    
    with app.app_context():
        # Test-brukere
        test_users = [
            {'username': 'audun', 'email': 'audun@test.no'},
            {'username': 'seba', 'email': 'seba@test.no'},
            {'username': 'marius', 'email': 'marius@test.no'},
            {'username': 'ingrid', 'email': 'ingrid@test.no'},
            {'username': 'lars', 'email': 'lars@test.no'},
        ]
        
        print("🔐 Oppretter test-brukere...")
        print("=" * 50)
        
        for user_data in test_users:
            # Sjekk om bruker finnes allerede
            existing = User.query.filter_by(username=user_data['username']).first()
            if existing:
                print(f"⏭️  {user_data['username']} finnes allerede - hopper over")
                continue
            
            # Opprett bruker
            user = User(
                username=user_data['username'],
                email=user_data['email']
            )
            
            # Sett passord: brukernavn + 123
            password = user_data['username'] + '123'
            user.set_password(password)
            
            db.session.add(user)
            print(f"✅ {user_data['username']:12} / {password}")
        
        db.session.commit()
        
        print("=" * 50)
        print(f"\n✨ Test-brukere opprettet!\n")
        
        # Vis alle brukere
        print("📋 Alle brukere i databasen:")
        print("-" * 50)
        for user in User.query.all():
            print(f"  • {user.username:12} ({user.email:20}) - Opprettet: {user.created_at}")
        print()

if __name__ == '__main__':
    setup_test_users()
