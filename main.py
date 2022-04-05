from flask import Flask, render_template, url_for, Blueprint, session, request, redirect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    SelectField, DecimalField, DateField, EmailField
from wtforms.validators import DataRequired, NumberRange
from connectBDD import DBSingleton
from insertion import ajouterEntreprise
from login import LogUser,log,is_valid_session
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

    class FormulaireCreationCom(FlaskForm):
        auteur = StringField("Auteur", validators=[DataRequired()])
        description = StringField("Description de l'entreprise",validators=[DataRequired()])
        date = DateField("Date du commentaire",validators=[DataRequired()])
        valider = SubmitField('Valider')

    class BarreDeRecherche(FlaskForm):
        filtre = StringField("Nom du contact", validators=[DataRequired()])
        valider = SubmitField('Valider')

    @app.route('/form', methods=['GET', 'POST'])
    def ajoutEntreprise():
        if is_valid_session:
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


    def stringer(tuple):
        return str(tuple).strip("(),")


    def getidentreprise(nom):
        tab: tuple = (nom,)
        sql = "SELECT identreprise FROM entreprise WHERE nom = %s;"
        reponse = db.query(sql, tab)
        identreprise = reponse[0]
        return stringer(identreprise)

    def getidcontact(nom):
        tab: tuple = (nom,)
        sql = "SELECT idpersonne FROM personne WHERE nom = %s;"
        reponse = db.query(sql, tab)
        idpersonne = reponse[0]
        return stringer(idpersonne)

    @app.route('/ajout-contact', methods=['GET', 'POST'])
    def ajoutContact():
        if is_valid_session:
            sql = "SELECT nom FROM entreprise"
            db.query(sql, )
            reponse = db.query(sql, )
            if reponse == []:
                print("pas d'entreprise donc pas de contacts")
            else:
                if request.method == 'POST':
                    nom = request.form['nom']
                    prenom = request.form['prenom']
                    email = request.form['email']
                    poste = request.form['poste']
                    telephone = request.form['telephone']
                    print(request.form)
                    actif = 1 if 'statut' in request.form else 0
                    entreprise = getidentreprise(request.form['entreprise'])
                    record = (nom, prenom, email, poste, telephone, actif, entreprise)
                    print(record)
                    try:
                        sql = """INSERT INTO personne (nom, prenom, email, poste, telephone, statut, entreprise_identreprise) 
                                    VALUES ('%s', '%s', '%s', '%s', %s, '%s', %s);""" % record
                        db_instance = DBSingleton.Instance()
                        db_instance.query(sql)
                    except:
                        print('pas bon')
            retourner = render_template('contactForm.html', reponses=reponse)
        return retourner


    @app.route('/', methods=['POST', 'GET'])
    def appeLogin():
        return LogUser()

    @app.route('/user', methods=['POST', 'GET'])
    def user():
        if is_valid_session:
            title = 'formulaire'
            sql = """SELECT nom,NSiret,adressePostale,codePostal,ville,description,url,COUNT(numeroFacture) FROM entreprise LEFT JOIN facture ON identreprise = facture.entreprise_identreprise GROUP BY nom ORDER BY nom"""
            db_instance = DBSingleton.Instance()
            posts = db_instance.query(sql)
            retourner = render_template('interface.html', title=title, posts=posts)
        return retourner


    @app.route('/del', methods=['POST', 'GET'])
    def deluser():
        title = 'formulaire'
        sql = """SELECT nom,NSiret,adressePostale,codePostal,ville,description,url,identreprise,COUNT(numeroFacture) FROM entreprise LEFT JOIN facture ON identreprise = facture.entreprise_identreprise GROUP BY nom ORDER BY nom"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('delentreprise.html', title=title, posts=posts)
        if request.method == "POST":
            ID = request.form['post_id']
            sql = f"DELETE FROM entreprise WHERE identreprise NOT IN (SELECT entreprise_identreprise FROM facture) AND identreprise = {ID}"
            print(sql)
            db_instance = DBSingleton.Instance()
            db_instance.query(sql)
            print('bon')
            retourner = redirect('/user')
        return retourner


    @app.route('/contact', methods=['POST', 'GET'])
    def contact():
        title = 'formulaire'
        sql = """SELECT  personne.nom,prenom,email,poste,telephone,statut,entreprise.nom AS 'nom entreprise' FROM personne JOIN entreprise ON entreprise_identreprise=entreprise.identreprise"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('interfacecontact.html', title=title, posts=posts)
        form = BarreDeRecherche()
        if form.validate_on_submit():
            recherche = request.form["filtre"]
            sql = f"SELECT nom,email FROM personne WHERE nom OR email LIKE '{recherche}%'"
            print(sql)
            db_instance = DBSingleton.Instance()
            db_instance.query(sql)
            print('bon')
        return retourner


    @app.route('/modif-contact', methods=['POST', 'GET'])
    def modifcontact():
        title = 'formulaire'
        sql = """SELECT  personne.nom,prenom,email,poste,telephone,statut,entreprise.nom AS 'nom entreprise',idpersonne FROM personne JOIN entreprise ON entreprise_identreprise=entreprise.identreprise"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('modifcontact.html', title=title, posts=posts)
        return retourner



    @app.route('/com', methods=['POST', 'GET'])
    def commentaire():
        title = 'formulaire'
        sql = """SELECT  auteur,description,dateDeCreation FROM commentaire ORDER BY dateDeCreation"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('interfacecom.html', title=title, posts=posts)
        return retourner
    @app.route('/ajout-com', methods=['POST', 'GET'])
    def ajoutcom():
        title = 'formulaire'
        sql = "SELECT auteur FROM commentaire"
        db.query(sql, )
        reponse = db.query(sql, )
        if reponse == []:
            print("pas d'entreprise donc pas de contacts")
        else:
            if request.method == 'POST':
                auteur = request.form['auteur']
                description = request.form['description']
                date = request.form['date']
                print(request.form)
                contact = getidcontact(request.form['contact'])
                record = (auteur, description, date, contact)
                print(record)
                try:
                    sql = """INSERT INTO commentaire (auteur, description, dateDeCreation, personne_idpersonne) 
                                                VALUES ('%s', '%s', '%s', '%s');""" % record
                    db_instance = DBSingleton.Instance()
                    db_instance.query(sql)
                except:
                    print('pas bon')
            retourner = render_template('comForm.html')
            return retourner

app.run(debug=True)