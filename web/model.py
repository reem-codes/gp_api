"""ORM=> Object Relational Mapping"""
from web import db
from dataclasses import dataclass
from datetime import datetime


class Base:
    id: int
    updateAt: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    updateAt = db.Column(db.DateTime, default=datetime.utcnow)

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
        obj.updateAt = datetime.utcnow()
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def put(cls, ids, kw):
        obj = cls.query.filter_by(**ids).first_or_404()
        for k in kw:
            obj.__setattr__(k, kw[k])
        obj.updateAt = datetime.utcnow()
        db.session.commit()
        return obj


@dataclass
class Configuration(db.Model, Base):
    id: int
    updateAt: str
    name: str
    desc: str
    hardware_id: int

    name = db.Column(db.String)
    desc = db.Column(db.Text)

    hardware_id = db.Column(db.Integer, db.ForeignKey('hardware.id', ondelete="cascade", onupdate="cascade"))
    commands = db.relationship("Command", backref="configuration", lazy='dynamic')
    # hardware = db.relationship("Hardware", uselist=False, foreign_keys=[hardware_id], back_populates="configurations")


@dataclass
class Hardware(db.Model, Base):
    id: int
    updateAt: str
    name: str
    icon: str
    desc: str
    gpio: int
    status_id: int

    name = db.Column(db.String)
    icon = db.Column(db.String)
    desc = db.Column(db.Text)
    gpio = db.Column(db.Integer)

    commands = db.relationship("Command", backref="hardware", lazy='dynamic')

    status_id = db.Column(db.Integer, db.ForeignKey('configuration.id'), nullable=True)
    status = db.relationship("Configuration", foreign_keys=[status_id], post_update=True)
    configurations = db.relationship("Configuration", foreign_keys=[Configuration.hardware_id], backref="hardware")


@dataclass
class Command(db.Model, Base):
    id: int
    updateAt: str
    hardware_id: int
    configuration_id: int
    schedule_id: int

    hardware_id = db.Column(db.Integer, db.ForeignKey('hardware.id', ondelete="cascade", onupdate="cascade"))
    configuration_id = db.Column(db.Integer, db.ForeignKey('configuration.id', ondelete="cascade", onupdate="cascade"))

    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=True)
    schedule = db.relationship("Schedule", foreign_keys=[schedule_id], post_update=True)

    responses = db.relationship("Response", backref="command", lazy='dynamic')


@dataclass
class Schedule(db.Model, Base):
    id: int
    updateAt: str
    days: int
    time: str

    days = db.Column(db.Integer)
    time = db.Column(db.Time)


@dataclass
class Response(db.Model, Base):
    id: int
    updateAt: str
    isDone: bool
    message: str
    executionTime: str
    isRead: bool
    command_id: int

    isDone = db.Column(db.Boolean)
    message = db.Column(db.String)
    executionTime = db.Column(db.DateTime)
    isRead = db.Column(db.Boolean)

    command_id = db.Column(db.Integer, db.ForeignKey('command.id', ondelete="cascade", onupdate="cascade"))
