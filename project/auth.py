from flask import Flask
from . import db
from flask import render_template
from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return render_template("login.html")
