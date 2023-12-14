from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user
# Import the auth Blueprint


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Handle registration logic based on the role
        if form.role.data == 'patient':
            flash('Patient account created for {}!'.format(form.username.data), 'success')
            return redirect(url_for('home'))
        elif form.role.data == 'doctor':
            flash('Doctor account created for {}!'.format(form.username.data), 'success')
            return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Handle login logic
        flash('Login successful for {}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)

@app.route('/register/doctor', methods=['GET', 'POST'])
def register_doctor():
    form = DoctorRegisterForm()

    if form.validate_on_submit():
        # Handle doctor registration logic
        flash('Doctor account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))

    return render_template('register_doctor.html', title='Doctor Register', form=form)
