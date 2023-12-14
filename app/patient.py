from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'  # Corrected the database name
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    illness = db.Column(db.String(200), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Patient {self.id}: {self.name}, {self.illness}, {self.symptoms}>'
    
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        illness = request.form['illness']
        symptoms = request.form['symptoms']

        new_patient = Patient(name=name, illness=illness, symptoms=symptoms)

        try:
            db.session.add(new_patient)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding the patient."

    else:
        patients = Patient.query.order_by(Patient.date_created).all()
        return render_template('patient.html', patients=patients)

if __name__ == '__main__':
    # Run the Flask application
    app.run(port=5000, debug=True)
