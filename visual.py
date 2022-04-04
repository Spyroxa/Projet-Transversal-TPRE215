from connectBDD import DBSingleton
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap


def User():
    cookie = session['user']['info']
    if cookie[0] == 0 and cookie[3] is True:
        title = 'formulaire'
        sql = """SELECT nom,n°siret,adressePostale,codePostal,ville,description,url FROM entreprise ORDER BY nom"""
        db_instance = DBSingleton.Instance()
        posts = db_instance.query(sql)
        retourner = render_template('interface.html', title=title, posts=posts)
        return retourner


