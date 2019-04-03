from flask import render_template, flash, redirect, url_for, request
from web_app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import pika
from web_app.forms import RegistrationForm, LoginForm
from web_app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'ashly'}

    return render_template('index.html', user=user, title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        text = user.get_auth_token()
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # !!!!!
        channel = connection.channel()
        channel.queue_declare(queue='confirming_email')
        channel.basic_publish(exchange='',
                              routing_key='confirming_email',
                              body=email+' http://127.0.0.1:5000/confirm/'+text)
        connection.close()
        flash('Now, check your mailbox')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)




@app.route('/confirm', methods=['GET', 'POST'])
@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm(token=None):
    user = User()
    if (token):
        if user.load_user(token):
            db.session.add(user)
            db.session.commit()
            render_template('nsr.html', token=token)
            return render_template('confirmation.html', title='Confirmed')

    else:
        flash('wtf!')
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

