"""ORM=> Object Relational Mapping"""
from web import db
from dataclasses import dataclass


class Base:
    @classmethod
    def get(cls, ids):
        obj = cls.query.filter_by(**ids).first_or_404()
        return obj

    @classmethod
    def index(cls, ids=None):
        obj = cls.query
        if ids:
            obj = obj.filter_by(**ids)
        obj = obj.all()
        return obj

    @classmethod
    def delete(cls, ids):
        obj = cls.query.filter_by(**ids).first_or_404()
        db.session.delete(obj)
        db.session.commit()
        return

    @classmethod
    def post(cls, kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def put(cls, ids, kw):
        obj = cls.query.filter_by(**ids).first_or_404()
        for k in kw:
            obj.__setattr__(k, kw[k])
        db.session.commit()
        return obj


@dataclass
class Hardware(db.Model, Base):
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

