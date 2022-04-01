from flask import Flask, render_template, url_for, Blueprint
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, NumberRange
from connectBDD import DBSingleton
from insertion import ajouterEntreprise
if __name__ == '__main__':
    app = Flask(__name__)
    Bootstrap(app)
    db = DBSingleton.Instance()
    app.config['SECRET_KEY'] = 'this is not a secret'

    def verificationEntreprise(nom):
        lenom: tuple = (nom,)
        sql = "SELECT id FROM entreprise WHERE nom = %s;"
        db.query(sql, lenom)
        if db.result == []:
            return False
        else:
            return True

    class FormulaireCreationEntreprise(FlaskForm):

        nom = StringField("Nom de l'entreprise", validators=[DataRequired()])
        numSiret = StringField("numero de siret", validators=[DataRequired()])
        adressePostale = StringField("adresse principale de l'entreprise", validators=[DataRequired()])
        codePostal = StringField("Code postal", validators=[DataRequired()])
        ville = StringField("ville de location", validators=[DataRequired()])
        description = StringField("description de l'entreprise", )
        url = StringField("url du site" , )
        valider = SubmitField('Valider')


    @app.route('/form', methods=['GET', 'POST'])
    def ajoutEntreprise():
        form = FormulaireCreationEntreprise()
        if form.validate_on_submit():
            params: tuple = (
            form.nom.data, form.numSiret.data, form.adressePostale.data,
            form.codePostal.data, form.ville.data,
            form.description.data, form.url.data)

            sql = "INSERT INTO entreprise (nom, NSiret, adressePostale, codePostal, ville, description, url) VALUES (%s,%s,%s,%s,%s,%s,%s); "
            db.query(sql, params)
            print("t'es un putain de génie")
        else:
            print(" ca marche pas")

        return render_template('login.html', form=form)
app.run(debug=True)