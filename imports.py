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
import time