from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from flask_migrate import Migrate
import os
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired

current_directory = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_directory, '..'))
datebasePath = os.path.join(project_root, 'db', 'site.db')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{datebasePath}"
app.config['SECRET_KEY'] = 'your_secret_key_here'

csrf = CSRFProtect(app)
db = SQLAlchemy(app)


# Определение класса для формы входа
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Определение класса для модели пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

class AddUserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    phoneNumber = StringField('phoneNumber', validators=[DataRequired()])
    balance = IntegerField('balance', validators=[DataRequired()])
    subscriptionType = StringField('subscriptionType', validators=[DataRequired()])
    subcribeEndDate = DateField('subscriptionEndDate', validators=[DataRequired()])
    submit = SubmitField('Add User')

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100))
    phoneNumber = db.Column(db.String(20))
    balance = db.Column(db.Integer)
    subscriptionType = db.Column(db.String(10))
    subcribeEndDate = db.Column(db.Date)

    def __repr__(self):
	    return "<{}:{}>".format(id, self.name)
    
with app.app_context():
    db.create_all()


# Определение менеджера входа
login_manager = LoginManager(app)
migrate = Migrate(app, db)

# Маршруты и функции представления
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adminpanel')
@login_required
def adminpanel():
    return render_template('adminpanel.html')

@app.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    form = AddUserForm()
    if form.validate_on_submit():
        name = form.name.data
        phoneNumber = form.phoneNumber.data
        balance = form.balance.data
        subscriptionType = form.subscriptionType.data
        subcribeEndDate = form.subcribeEndDate.data

        existing_user = Users.query.filter_by(phoneNumber=phoneNumber).first()
        if existing_user:
            return render_template('adduser.html', form=form, text='Користувач з таким номером вже існує.')
        
        user = Users(name=name, phoneNumber=phoneNumber, balance=balance, subscriptionType=subscriptionType, subcribeEndDate=subcribeEndDate)
        db.session.add(user)
        db.session.commit()
        return render_template('adduser.html', form=form, text='Ви успішно додали користувача.')
    return render_template('adduser.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Использование определенной формы
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('adminpanel'))
        return render_template('login.html', form=form, condition=True)
    return render_template('login.html', form=form, condition=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)
