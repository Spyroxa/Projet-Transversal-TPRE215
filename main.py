from flask import Flask, render_template, redirect, url_for, flash, request, Blueprint, make_response, session
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is a not a secret'

if __name__ == '__main__':
    app.run(debug=True)

    class FormulaireCreationEntreprise(FlaskForm):

        nom = StringField("Nom de l'entreprise", validators=[DataRequired()])
        numSiret = StringField("numero de siret", validators=[DataRequired()])
        adressePostale = StringField('Prix de la visite', validators=[DataRequired()])
        codePostal = StringField("Date de l'étape", validators=[DataRequired()])
        ville = StringField("ville de location", validators=[DataRequired()])
        description = StringField("description de l'entreprise", validators=[DataRequired()])
        valider = SubmitField('Valider')


    @app.route('/valac/ajouter-une-entreprise/', methods=['GET', 'POST'])
    def ajoutEtape():
        formEntreprise = FormulaireCreationEntreprise()
        if formEntreprise.validate_on_submit():
            return("t'es trop fort mec")
        else:
            return("crotte")

app.run(debug=True)