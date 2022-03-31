from flask import Flask, render_template, url_for, Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, NumberRange
from connectBDD import DBSingleton

if __name__ == '__main__':
    app = Flask(__name__)
    db = DBSingleton.Instance()
    app.config['SECRET_KEY'] = 'this is not a secret'

    class FormulaireCreationEntreprise(FlaskForm):

        nom = StringField("Nom de l'entreprise", validators=[DataRequired()])
        numSiret = StringField("numero de siret", validators=[DataRequired()])
        adressePostale = StringField('Prix de la visite', validators=[DataRequired()])
        codePostal = StringField("Date de l'étape", validators=[DataRequired()])
        ville = StringField("ville de location", validators=[DataRequired()])
        description = StringField("description de l'entreprise", validators=[DataRequired()])
        valider = SubmitField('Valider')


    @app.route('/form', methods=['GET', 'POST'])
    def ajoutEntreprise():
        render_template('login.html')

app.run(debug=True)