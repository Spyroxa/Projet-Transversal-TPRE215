from imports import *

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
    email = EmailField("Email du contact", validators=[DataRequired()])
    poste = StringField("Prenom du contact", validators=[DataRequired()])
    valider = SubmitField('Valider')


class FormulaireCreationCom(FlaskForm):
    auteur = StringField("Auteur", validators=[DataRequired()])
    description = StringField("Description du prospect", validators=[DataRequired()])
    date = DateField("Date du commentaire", validators=[DataRequired()])
    valider = SubmitField('Valider')


class BarreDeRecherche(FlaskForm):
    filtre = StringField("Nom du contact", validators=[DataRequired()])
    valider = SubmitField('Valider')