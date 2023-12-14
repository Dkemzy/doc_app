from app import app, db
from models import User, Patient  # Import both User and Patient models

# Create the tables within the application context
with app.app_context():
    db.create_all()

    # Optional: Seed initial data
    with db.session.begin():
        # Code to insert initial data into User and Patient tables
        admin_user = User(username='Victor', email='admin@example.com', password='admin_password', role='doctor')
        patient_user = User(username='Dennis', email='patient@example.com', password='patient_password', role='patient')

        db.session.add(admin_user)
        db.session.add(patient_user)
        
        patient_1 = Patient(name='Malaria', illness='Cold', symptoms='Headache, Fatigue, Body heat')
        patient_2 = Patient(name='Fever', illness='Fever', symptoms='Cough,Headache, Fatigue')
        
        db.session.add(patient_1)
        db.session.add(patient_2)
        
        db.session.commit()