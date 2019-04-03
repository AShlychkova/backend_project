from flask import render_template, flash, redirect, url_for, request
from web_app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import pika
from itsdangerous import URLSafeTimedSerializer

from web_app import models
from web_app.forms import EmptyForm, RegistrationForm, LoginForm
from web_app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'ashly'}
    posts = [
            {
                'author': {'username': 'John'},
                'body': 'Beautiful day in Portland!'
            },
            {
                'author': {'username': 'Susan'},
                'body': 'The Avengers movie was so cool!'
            }]
    return render_template('index.html', user=user, title='Home', posts=posts)


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


@app.route('/nsr')
def nsr():
    flash('Thanks for registration')
    form = EmptyForm()
    return render_template('nsr.html', form=form)


@app.route('/send_conf_link', methods=['GET', 'POST'])
def send_conf_link():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    safe = URLSafeTimedSerializer(config.SECRET_KEY)
    if form.validate_on_submit():
        email = form.email.data
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))# !!!!!
        channel = connection.channel()
        channel.queue_declare(queue='confirming_email')
        channel.basic_publish(exchange='',
                              routing_key='confirming_email',
                              body=email)
        connection.close()
    return redirect(url_for('index'))


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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route
def load_token(token):
    max_age = config.TOCKEN_DURATION.total_seconds()
    data = models.login_serializer.loads(token, max_age=max_age)
    if data:
        return 1
    return 0
