"""ORM=> Object Relational Mapping"""
from web import db
from dataclasses import dataclass


@dataclass
class Hardware(db.Model):
    id: int
    name: str
    icon: str
    desc: str
    gpio: int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)
    desc = db.Column(db.Text)
    gpio = db.Column(db.Integer)



@dataclass
class Config(db.Model):
    id: int
    name: str
    icon: str
    desc: str
    gpio: int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)
    desc = db.Column(db.Text)
    gpio = db.Column(db.Integer)
