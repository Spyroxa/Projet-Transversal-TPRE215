from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField, IntegerField, SelectField, DecimalField, PasswordField, \
    EmailField,TextAreaField
from wtforms.validators import DataRequired, NumberRange
from connectBDD import DBSingleton

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is not a secret'
Bootstrap(app)


class authForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    MDP = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Submit')
    session_LOGIN = None
    Session_MDP = None
    Session_id = None


def log():
    form = authForm()
    cookie = False
    retourner = [None, None, None, cookie]
    if form.validate_on_submit():
        login = request.form.get('login')
        MDP = request.form.get('motDePasse')
        sql = f"SELECT login FROM utilisateur WHERE login = '{login}'"
        db_instance = DBSingleton.Instance()
        temp = db_instance.query(sql)
        if len(temp) == 0:
            print('vide')
        else:
            true_login = temp[0][0]
            if true_login == login:
                sql = f"SELECT motDePasse FROM utilisateur WHERE login = '{login}'"
                db_instance = DBSingleton.Instance()
                temp = db_instance.query(sql)
                password = temp[0][0]
                """mot de passe prit part le insert"""
                if password == MDP:
                    sql = f"SELECT id.utilisateur AS ID FROM utilisateur WHERE login = '{login}' AND motDePasse = '{MDP}'"
                    db_instance = DBSingleton.Instance()
                    temp = db_instance.query(sql)
                    ID = temp[0][0]
                    cookie = True
                    retourner = [ID, login, MDP, cookie]
                    session['user'] = {"info": retourner}
                    print(f"le mot de passe session est {retourner}")
                else:
                    print("pas bon mdp")
    return retourner

def LogUser():
    cookie = log()
    form = authForm()
    ID = cookie[0]
    print(cookie)
    session['user'] = {"info": cookie}
    print(session['user']['info'])
    title = 'login'
    result = render_template('user.html', form=form, title=title)
    if cookie[0] is True:
        result = redirect('/user')
    return result



if __name__ == '__main__':
    app.run(debug=True)