import sys
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request, jsonify, redirect, url_for, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:WierdScience#23\
@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

association_table = db.Table(
    "association_table",
    db.Column("surgery_mrn", db.Integer, db.ForeignKey(
        "surgery.mrn"), primary_key=True),
    db.Column("cath_mrn", db.Integer, db.ForeignKey(
        "cath.mrn"), primary_key=True)
)
