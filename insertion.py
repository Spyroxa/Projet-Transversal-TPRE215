from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField, IntegerField, SelectField, DecimalField, DateField, \
    PasswordField, EmailField
from wtforms.validators import DataRequired, NumberRange
from connectBDD import DBSingleton

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is a secret'
Bootstrap(app)


class InsertUserForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    siret = StringField('Siret', validators=[DataRequired()])
    adresse = StringField('Adresse', validators=[DataRequired()])
    code_postal = StringField('mot de passe ?', validators=[DataRequired()])
    ville = StringField('ville',validators=[DataRequired()])
    description = StringField('Description')
    url = StringField('url')
    submit = SubmitField('Submit')


def ajouterEntreprise():
    form = InsertUserForm()
    title = 'formulaire'
    retourner = render_template('login.html', form=form, title=title)
    if form.validate_on_submit():
        nom = form.nom.data
        siret = form.siret.data
        adresse = form.adresse.data
        code_postal = form.code_postal.data
        ville = form.ville.data
        description = form.description.data
        url = form.url.data
        record = (nom, siret, adresse, code_postal, ville, description, url)
        sql = "INSERT INTO entreprise ( nom,n°siret, adressePostal, codePostal, ville, description, url) VALUES ('%s','%s','%s','%s','%s',%s);" % record
        db_instance = DBSingleton.Instance()
        db_instance.query(sql)
        retourner = redirect('/form')
    return retourner


if __name__ == '__main__':
    app.run(debug=True)
