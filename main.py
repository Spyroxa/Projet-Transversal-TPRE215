from flask import Flask, render_template, url_for, Blueprint, session, request, redirect,send_file
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    SelectField, DecimalField, DateField, EmailField
from wtforms.validators import DataRequired, NumberRange
from connectBDD import DBSingleton
from insertion import ajouterEntreprise
from login import LogUser,log,is_valid_session
from visual import User
from flask import render_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas




if __name__ == '__main__':
    app = Flask(__name__)
    Bootstrap(app)
    db = DBSingleton.Instance()
    app.config['SECRET_KEY'] = 'this is not a secret'

    def verificationprospect(nom):
        lenom: tuple = (nom,)
        sql = "SELECT id FROM prospect WHERE nom = %s;"
        db.query(sql, lenom)
        if db.result == []:
            return False
        else:
            return True

    def verificationContactDejaExistant(nom):
        contact: tuple = (nom,)
        sql = "SELECT nom FROM contact WHERE nom = %s;"
        reponse = db.query(sql, contact)
        if reponse == []:
             return False
        else:
             return True

    class FormulaireCreationprospect(FlaskForm):

        nom = StringField("Nom du prospect", validators=[DataRequired()])
        numSiret = StringField("Numero de siret", validators=[DataRequired()])
        adressePostale = StringField("Adresse principale du prospect", validators=[DataRequired()])
        codePostal = StringField("Code postal", validators=[DataRequired()])
        ville = StringField("Ville de location", validators=[DataRequired()])
        description = StringField("Description du prospect", )
        url = StringField("Url du site", )
        valider = SubmitField('Valider')


    class FormulaireCreationContact(FlaskForm):
        nom = StringField("Nom du contact", validators=[DataRequired()])
        prenom = StringField("Prenom du contact", validators=[DataRequired()])
        email = EmailField ("Email du contact", validators=[DataRequired()])
        poste = StringField("Prenom du contact", validators=[DataRequired()])
        valider = SubmitField('Valider')

    class FormulaireCreationCom(FlaskForm):
        auteur = StringField("Auteur", validators=[DataRequired()])
        description = StringField("Description du prospect",validators=[DataRequired()])
        date = DateField("Date du commentaire",validators=[DataRequired()])
        valider = SubmitField('Valider')

    class BarreDeRecherche(FlaskForm):
        filtre = StringField("Nom du contact", validators=[DataRequired()])
        valider = SubmitField('Valider')

    @app.route('/form', methods=['GET', 'POST'])
    def ajoutprospect():
        if is_valid_session:
            form = FormulaireCreationprospect()
            if form.validate_on_submit():
                params: tuple = (
                form.nom.data, form.numSiret.data, form.adressePostale.data,
                form.codePostal.data, form.ville.data,
                form.description.data, form.url.data)

                sql = "INSERT INTO prospect (nom, NSiret, adressePostale, codePostal, ville, description, url) VALUES (%s,%s,%s,%s,%s,%s,%s); "
                db.query(sql, params)
                print("ça marche")
            else:
                print(" ça marche pas")

        return render_template('login.html', form=form)


    def stringer(tuple):
        return str(tuple).strip("(),")


    def getidprospect(nom):
        tab: tuple = (nom,)
        sql = "SELECT idprospect FROM prospect WHERE nom = %s;"
        reponse = db.query(sql, tab)
        idprospect = reponse[0]
        return stringer(idprospect)

    def getidcontact(nom):
        tab: tuple = (nom,)
        sql = "SELECT idcontact FROM contact WHERE nom = %s;"
        reponse = db.query(sql, tab)
        idcontact = reponse[0]
        return stringer(idcontact)

    @app.route('/ajout-contact', methods=['GET', 'POST'])
    def ajoutContact():
        if is_valid_session:
            sql = "SELECT nom FROM prospect"
            db.query(sql, )
            reponse = db.query(sql, )
            if reponse == []:
                print("pas de prospect donc pas de contacts")
            else:
                if request.method == 'POST':
                    nom = request.form['nom']
                    prenom = request.form['prenom']
                    email = request.form['email']
                    poste = request.form['poste']
                    telephone = request.form['telephone']
                    print(request.form)
                    actif = 1 if 'statut' in request.form else 0
                    prospect = getidprospect(request.form['prospect'])
                    record = (nom, prenom, email, poste, telephone, actif, prospect)
                    print(record)
                    try:
                        sql = """INSERT INTO contact (nom, prenom, email, poste, telephone, statut, prospect_idprospect) 
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
            sql = """SELECT nom,NSiret,adressePostale,codePostal,ville,description,url,COUNT(numeroFacture) FROM prospect LEFT JOIN facture ON idprospect = facture.prospect_idprospect GROUP BY nom ORDER BY nom"""
            db_instance = DBSingleton.Instance()
            posts = db_instance.query(sql)
            retourner = render_template('interface.html', title=title, posts=posts)
        return retourner


    @app.route('/del', methods=['POST', 'GET'])
    def deluser():
        title = 'formulaire'
        sql = """SELECT nom,NSiret,adressePostale,codePostal,ville,description,url,idprospect,COUNT(numeroFacture) FROM prospect LEFT JOIN facture ON idprospect = facture.prospect_idprospect GROUP BY nom ORDER BY nom"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('delentreprise.html', title=title, posts=posts)
        if request.method == "POST":
            ID = request.form['post_id']
            sql = f"DELETE FROM prospect WHERE idprospect NOT IN (SELECT prospect_idprospect FROM facture) AND idprospect = {ID}"
            print(sql)
            db_instance = DBSingleton.Instance()
            db_instance.query(sql)
            print('bon')
            retourner = redirect('/user')
        return retourner


    @app.route('/contact', methods=['POST', 'GET'])
    def contact():
        title = 'formulaire'
        sql = """SELECT  contact.nom,prenom,email,poste,telephone,statut,prospect.nom AS 'nom prospect' FROM contact JOIN prospect ON prospect_idprospect=prospect.idprospect"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('interfacecontact.html', title=title, posts=posts)
        form = BarreDeRecherche()
        if form.validate_on_submit():
            recherche = request.form["filtre"]
            sql = f"SELECT nom,email FROM contact WHERE nom OR email LIKE '{recherche}%'"
            print(sql)
            db_instance = DBSingleton.Instance()
            db_instance.query(sql)
            print('bon')
        return retourner


    @app.route('/editer-contact', methods=['GET', 'POST'])
    def modifContact():
        sql = "SELECT nom FROM contact"
        db.query(sql, )
        reponse = db.query(sql, )
        if verificationContactDejaExistant(reponse) == True:
            if request.method == 'POST':
                nom = request.form['nom']
                prenom = request.form['prenom']
                email = request.form['email']
                poste = request.form['poste']
                telephone = request.form['telephone']
                actif = 1 if 'statut' in request.form else 0
                prospect = getidprospect(request.form['prospect'])
                record = (nom, prenom, email, poste, telephone, actif, prospect)
            sql = "UPDATE contact SET nom = '%s', prenom = '%s', email = '%s', " \
                  "poste = '%s', telephone = %s, actif = %s, " \
                  "prospect = '%s',  " % record
            db_instance = DBSingleton.Instance()
            db_instance.query(sql)
            retourner = render_template('contactForm.html', reponses=reponse)
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
            print("pas d'prospect donc pas de contacts")
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
                    sql = """INSERT INTO commentaire (auteur, description, dateDeCreation, contact_idcontact) 
                                                VALUES ('%s', '%s', '%s', '%s');""" % record
                    db_instance = DBSingleton.Instance()
                    db_instance.query(sql)
                except:
                    print('pas bon')
        retourner = render_template('comForm.html')
        return retourner



    # @app.route('/pdf/<facture_id>')
    #     def display_pdf(facture_id):
    #             return send_file('canvas_form.pdf', attachment_filename='file.pdf')
    #
    # @app.route('/facture', methods=['POST', 'GET'])
    #     def form(path, prospect_nom, nom_contact):
    #         my_canvas = canvas.Canvas(path, pagesize=letter)
    #         my_canvas.setLineWidth(.4)
    #         my_canvas.setFont('Helvetica', 12)
    #         my_canvas.drawString(30, 750, 'La jolie boite à code')
    #         my_canvas.drawString(30, 715, 'adresse : ')
    #         my_canvas.drawString(400, 680, 'FACTURE:')
    #         my_canvas.drawString(30, 700, 'adresse entreprise:')
    #         my_canvas.drawString(30, 640, 'N° de SIREN:')
    #         my_canvas.drawString(30, 590, f'Tel. :{prospect_nom}')
    #         my_canvas.drawString(30, 570, 'Email:')
    #         my_canvas.drawString(30, 550, 'IBAN:')
    #         my_canvas.drawString(30, 470, f'Numéro {nom_contact}:')
    #         my_canvas.drawString(160, 470, f'Date {nom_contact}:')
    #         my_canvas.drawString(350, 520, f'Nom du prospect : {prospect_nom} ')
    #         my_canvas.drawString(350, 500, f'Nom du contact : {nom_contact}')
    #         my_canvas.drawString(350, 480, f'Adresse du prospect :{prospect_nom}')
    #         my_canvas.drawString(350, 460, f'Code et Ville du prospect :{prospect_nom}')
    #         my_canvas.save()
    #     return send_file('canvas_form.pdf', attachment_filename='file.pdf')

    #if __name__ == '__main__':
     #   form('canvas_form.pdf', 'EPSI', ' PANNETIER_Magali')

app.run(debug=True)