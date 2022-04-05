from flask import Flask, render_template, url_for, Blueprint, session, request, redirect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    SelectField, DecimalField, DateField, EmailField
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
        numSiret = StringField("Numero de siret", validators=[DataRequired()])
        adressePostale = StringField("Adresse principale de l'entreprise", validators=[DataRequired()])
        codePostal = StringField("Code postal", validators=[DataRequired()])
        ville = StringField("Ville de location", validators=[DataRequired()])
        description = StringField("Description de l'entreprise", )
        url = StringField("Url du site" , )
        valider = SubmitField('Valider')


    class FormulaireCreationContact(FlaskForm):
        nom = StringField("Nom du contact", validators=[DataRequired()])
        prenom = StringField("Prenom du contact", validators=[DataRequired()])
        email = EmailField ("Email du contact", validators=[DataRequired()])
        poste = StringField("Prenom du contact", validators=[DataRequired()])
        valider = SubmitField('Valider')

    class BarreDeRecherche(FlaskForm):
        filtre = StringField("Nom du contact", validators=[DataRequired()])
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


    @app.route('/ajout-contact', methods=['GET', 'POST'])
    def ajoutContact():
        form = FormulaireCreationContact()
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
        sql = """SELECT nom,NSiret,adressePostale,codePostal,ville,description,url,COUNT(numeroFacture) FROM entreprise LEFT JOIN facture ON identreprise = facture.entreprise_identreprise GROUP BY nom ORDER BY nom"""
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
        sql = """SELECT  personne.nom,prenom,email,poste,telephone,statut,entreprise.nom AS 'nom entreprise' FROM personne JOIN entreprise ON entreprise_identreprise=entreprise.identreprise"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('interfacecontact.html', title=title, posts=posts)
        #if
        return retourner


    @app.route('/modif-contact', methods=['POST', 'GET'])
    def modifContact():
        title = 'formulaire'
        idpersonne = session['personne']['id']
        print(idpersonne)
        sql = """SELECT  nom,prenom,email,poste,telephone,statut FROM personne"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        sql = f"SELECT * FROM personne WHERE idpersonne = {idpersonne}"
        print(sql)
        db_instance = DBSingleton.Instance()
        tailles = db_instance.query(sql)
        print(tailles)
        retourner = render_template('modifcontact.html', title=title, posts=posts)
        if request.method == 'POST':
            statut = request.form['statut']
            try:
                sql = f"""UPDATE personne
                           SET statut = '{statut}', 
                           WHERE idpersonne = {idpersonne};"""
                db_instance = DBSingleton.Instance()
                db_instance.query(sql)
                print("good")
                retourner = redirect("/admin-circuit")
            except:
                print("faux")
        else:
            retourner = redirect('/')
        return retourner


    @app.route('/com', methods=['POST', 'GET'])
    def Commentaire():
        title = 'formulaire'
        sql = """SELECT  auteur,description,dateDeCreation FROM commentaire ORDER BY dateDeCreation"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('interfacecom.html', title=title, posts=posts)
        return retourner

app.run(debug=True)