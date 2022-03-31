from flask import Flask, render_template, redirect, url_for, flash, request, Blueprint, make_response, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is a not a secret'

if __name__ == '__main__':
    app.run(debug=True)
