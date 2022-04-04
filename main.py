from flask import Flask, render_template, url_for, Blueprint, session, request, redirect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, NumberRange
from connectBDD import DBSingleton
from insertion import ajouterEntreprise
from login import LogUser,log
from visual import User
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
            print("ça marche")
        else:
            print(" ça marche pas")

        return render_template('login.html', form=form)


    @app.route('/', methods=['POST', 'GET'])
    def appeLogin():
        return LogUser()

    @app.route('/user', methods=['POST', 'GET'])
    def User():
        title = 'formulaire'
        sql = """SELECT nom,NSiret,adressePostale,codePostal,ville,description,url,COUNT(numeroFacture) FROM entreprise JOIN facture ON identreprise = facture.entreprise_identreprise"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('interface.html', title=title, posts=posts)
        return retourner


    @app.route('/del', methods=['POST', 'GET'])
    def delUser():
        title = 'formulaire'
        sql = """SELECT nom,NSiret,adressePostale,codePostal,ville,description,url,identreprise FROM entreprise"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('delentreprise.html', title=title, posts=posts)
        if request.method == "POST":
            id = request.form['identreprise']
            sql = f"DELETE FROM entreprise WHERE identreprise NOT IN (SELECT entreprise_identreprise FROM facture) AND identreprise =  {id}"
            print(sql)
            db_instance = DBSingleton.Instance()
            db_instance.query(sql)
            print('bon')
            retourner = redirect('/user')
        return retourner


    @app.route('/contact', methods=['POST', 'GET'])
    def Contact():
        title = 'formulaire'
        sql = """SELECT  nom,prenom,email,poste,telephone,statut FROM personne"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('interfacecontact.html', title=title, posts=posts)
        return retourner


    @app.route('/com', methods=['POST', 'GET'])
    def Commentaire():
        title = 'formulaire'
        sql = """SELECT  auteur,description,dateDeCreation FROM commentaire"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('interfacecom.html', title=title, posts=posts)
        return retourner

app.run(debug=True)