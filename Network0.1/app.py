import flask
import configparser
from static.modules.DB.db import Database
from static.modules.Chekers.SQL_Injection_Checker import SQL_Injection_Checker
from static.modules.Chekers.password_check import pcheck
from static.modules.Chekers.filesAllow import check_file
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import ValidationError
from flask import Flask, render_template, url_for, redirect
from werkzeug.utils import secure_filename
import os

config = configparser.ConfigParser()
config.read('config.ini')
app = flask.Flask(__name__)
bcrypt = Bcrypt(app)
SQLAlchemydb = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

pathDB = config["DataBase"]["path"]
db = Database(path=pathDB)
db.CreateTableAllUsers()
db.close()

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config["SQLAlchemy"]["path"]}'
app.config['SECRET_KEY'] = config["Server"]['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = config['Server']['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LENGTH'] = 8 * 1000 * 1000

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(SQLAlchemydb.Model, UserMixin):
    id = SQLAlchemydb.Column(SQLAlchemydb.Integer, primary_key=True)
    username = SQLAlchemydb.Column(SQLAlchemydb.String(20), nullable=False, unique=True)
    contact = SQLAlchemydb.Column(SQLAlchemydb.String(50), nullable=False, unique=True)
    password = SQLAlchemydb.Column(SQLAlchemydb.String(80), nullable=False)

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

@app.route('/')
@app.route('/registration', methods=['POST', 'GET'])
def register():
    if flask.request.method == 'POST':
        name = flask.request.form['nameAndSurname']
        contact = flask.request.form['email']
        password = flask.request.form['password']
        print(f"[ Register ] :\n      {name}\n      {contact}\n      {password}")
        if all((name, contact, password)):
            if all((SQL_Injection_Checker(name), SQL_Injection_Checker(contact), SQL_Injection_Checker(password))):
                try:
                    hash_password = bcrypt.generate_password_hash(password)
                    db = Database(path=pathDB)
                    db.new(name, contact, hash_password)
                    db.close()
                    new_user = User(username=name, password=hash_password, contact=contact)
                    SQLAlchemydb.session.add(new_user)
                    SQLAlchemydb.session.commit()
                    return flask.redirect(f'/login')
                except Exception as e:
                    print(str(e))
                    return flask.render_template('registration.html', script='registerBad()')
            else:
                return flask.render_template('registration.html', script='registerBad()')
        else:
            return flask.render_template('registration.html', script='registerBad()')
    else:
        return flask.render_template('registration.html', script='')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if flask.request.method == 'POST':
        db = Database(path=pathDB)
        user = db.get_user(bcrypt=bcrypt, username=flask.request.form['nameAndSurname'], password=flask.request.form['password'])
        db.close()
        if user:
            user = User.query.filter_by(username=flask.request.form['nameAndSurname']).first()
            if user:
                login_user(user)
                return redirect(url_for("get_page"))
            return flask.render_template('login.html')
        else:
            return flask.render_template('login.html')
    else:
        return flask.render_template('login.html')


@app.route("/page")
@login_required
def get_page():
    info = Database(path=pathDB).get_user_info(current_user.username, close=True)
    return flask.render_template('page.html', info=info)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/dev-contact")
@login_required
def dev_contact():
    info = Database(path=pathDB).get_user_info(current_user.username, close=True)
    return flask.render_template('dev_contact.html', info=info)


@app.route("/dashbord")
@login_required
def dashbord():
    info = Database(path=pathDB).get_user_info(current_user.username, close=True)
    return flask.render_template('dashbord.html', info=info)


@app.route("/redactor", methods=['GET', 'POST'])
def redactor():
    if flask.request.method == 'POST':
        file = flask.request.files['file']
        print(os.getcwd())
        FileNameToSave = check_file(file.filename)
        if 'file' in flask.request.files and file.filename and FileNameToSave:
            # сохраняем файл
            file.save(os.path.join(os.getcwd() + app.config['UPLOAD_FOLDER'], FileNameToSave))
            Database(path=pathDB).updateMainPhotoPath(current_user.username, path=os.path.join(app.config['UPLOAD_FOLDER'], FileNameToSave), close=True)
        info = Database(path=pathDB).get_user_info(current_user.username, close=True)
        return flask.render_template('redactor.html', info=info)
    else:
        info = Database(path=pathDB).get_user_info(current_user.username, close=True)
        return flask.render_template('redactor.html', info=info)

if __name__ == '__main__':

    debug = config["Server"]["debug"]
    SQLAlchemydb.create_all()
    if debug == "True":
        app.run(debug=True, host="127.0.0.1", port=5000)
    else:
        app.run(host="92.63.100.2", port=5000, debug=False)