from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_login import login_required
from models import User, Patient, db

main = Blueprint('main', __name__)

bcrypt = Bcrypt()

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email_address']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        if not username or not email or not password or not confirm_password or not role:
            flash('All fields are required', 'danger')
            return redirect(url_for('main.register'))

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('main.register'))

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already exists. Please choose another one.', 'danger')
            return redirect(url_for('main.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful for {}!'.format(username), 'success')
        login_user(new_user)
        return redirect(url_for('main.home'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@main.route('/patients', methods=['GET', 'POST'])
@login_required
def patients():
    if request.method == 'POST':
        name = request.form['name']
        illness = request.form['illness']
        symptoms = request.form['symptoms']

        if not name or not illness or not symptoms:
            flash('All fields are required', 'danger')
            return redirect(url_for('main.patients'))

        new_patient = Patient(name=name, illness=illness, symptoms=symptoms)

        try:
            db.session.add(new_patient)
            db.session.commit()
            return redirect(url_for('main.patients'))
        except:
            return "There was an issue adding the patient."

    else:
        patients = Patient.query.order_by(Patient.date_created).all()
        return render_template('patient.html', patients=patients)
    
@main.route('/search', methods=['POST'])
def search_patients():
    illness = request.form.get('illness')
    search_results = []

    if illness:
        search_results = Patient.query.filter(Patient.illness.ilike(f"%{illness}%")).all()

    return render_template('patient.html', search_results=search_results)

# @main.route('/register_doctor', methods=['GET', 'POST'])
# def register_doctor():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email_address']
#         password1 = request.form['password1']
#         password2 = request.form['password2']
#         role = request.form['role']
#         specialization = request.form['specialization']
#         hospital = request.form['hospital']
#         experience_years = request.form['experience_years']

#         if not username or not email or not password1 or not password2 or not role:
#             flash('All fields are required', 'danger')
#             return redirect(url_for('main.register_doctor'))

#         if password1 != password2:
#             flash('Passwords do not match', 'danger')
#             return redirect(url_for('main.register_doctor'))

#         if Doctor.query.filter_by(username=username).first() or Doctor.query.filter_by(email=email).first():
#             flash('Username or email already exists. Please choose another one.', 'danger')
#             return redirect(url_for('main.register_doctor'))

#         hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
#         new_doctor = Doctor(username=username, email=email, password=hashed_password, role=role,
#                             specialization=specialization, hospital=hospital, experience_years=experience_years)
#         db.session.add(new_doctor)
#         db.session.commit()

#         flash('Doctor registration successful for {}!'.format(username), 'success')
#         return redirect(url_for('main.login'))

#     return render_template('register_doctor.html')

@main.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        valid_doctor = Doctor.query.filter_by(username=username).first()

        if valid_doctor and bcrypt.check_password_hash(valid_doctor.password, password):
            login_user(valid_doctor)
            flash('Doctor login successful!', 'success')
            return redirect(url_for('main.doctor'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('DoctorLoginForm.html')

@main.route('/delete/<int:id>')
def delete(id):
    patient_to_delete = Patient.query.get_or_404(id)

    try:
        db.session.delete(patient_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that patient."

@main.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        patient.name = request.form['name']
        patient.symptoms = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the patient.'

    return render_template('update.html', patient=patient)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in the {getattr(form, field).label.text} field - {error}', 'danger')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
