from web_app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from web_app import login_manager
from itsdangerous import URLSafeTimedSerializer
import config

login_serializer = URLSafeTimedSerializer(config.Config.SECRET_KEY)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_auth_token(self):
        data = ['^-^', str(self.password_hash),  str(self.username), str(self.email), str(config.Config.SALT)]
        return login_serializer.dumps(data)

    def load_user(self, token):
        max_age = config.Config.TOCKEN_DURATION
        data = login_serializer.loads(token, max_age=max_age)
        if len(data) == 5 and data[4] == config.Config.SALT:
            self.password_hash = data[1]
            self.username = data[2]
            self.email = data[3]
            return data[0]
        return 0


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))





