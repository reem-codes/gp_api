"""ORM=> Object Relational Mapping"""
from web import db, bcrypt
from dataclasses import dataclass
from datetime import datetime
"""
Each class represent a model i.e. a table in the database
all of the models inherits from the Base class, which has the CRUD methods
RevokedToken class is there for the logout token strings, part of the auth process
"""


class Base:
    id: int
    updateAt: datetime

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

#
# @dataclass
# class Configuration(db.Model, Base):
#     id: int
#     updateAt: datetime
#     name: str
#     desc: str
#     hardware_id: int
#
#     name = db.Column(db.String)
#     desc = db.Column(db.Text)
#
#     hardware_id = db.Column(db.Integer, db.ForeignKey('hardware.id', ondelete="cascade", onupdate="cascade"))
#     commands = db.relationship("Command", backref="configuration", lazy='dynamic')
#     # hardware = db.relationship("Hardware", uselist=False, foreign_keys=[hardware_id], back_populates="configurations")
#


@dataclass
class Hardware(db.Model, Base):
    id: int
    updateAt: datetime
    name: str
    icon: str
    desc: str
    gpio: int
    raspberry_id: int
    status: bool

    name = db.Column(db.String)
    icon = db.Column(db.String)
    desc = db.Column(db.Text)
    gpio = db.Column(db.Integer)
    raspberry_id = db.Column(db.Integer, db.ForeignKey('raspberry.id', ondelete="cascade", onupdate="cascade"))
    commands = db.relationship("Command", backref="hardware", lazy='dynamic')
    status = db.Column(db.Boolean)

    def __hash__(self):
        return hash(self.id)


@dataclass
class Schedule(db.Model, Base):
    id: int
    updateAt: datetime
    days: int
    time: str

    days = db.Column(db.Integer)
    time = db.Column(db.String)

    def __hash__(self):
        return hash(self.id)


@dataclass
class Command(db.Model, Base):
    id: int
    updateAt: datetime
    hardware_id: int
    configuration: bool
    schedule_id: int
    schedule: Schedule

    hardware_id = db.Column(db.Integer, db.ForeignKey('hardware.id', ondelete="cascade", onupdate="cascade"))

    configuration = db.Column(db.Boolean)

    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=True)
    schedule = db.relationship("Schedule", foreign_keys=[schedule_id], post_update=True)

    responses = db.relationship("Response", backref="command", lazy='dynamic')

    @classmethod
    def index(cls, ids=None, schedule_not_null=False):
        obj = cls.query
        if ids:
            obj = obj.filter_by(**ids)
        if schedule_not_null:
            print("inside not null")
            obj = obj.filter(cls.schedule_id.isnot(None))
        obj = obj.all()
        return obj

    def __hash__(self):
        return hash(self.id)


@dataclass
class Response(db.Model, Base):
    id: int
    updateAt: datetime
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

    def __hash__(self):
        return hash(self.id)


RaspberryUser = db.Table(
    'raspberry_user',
    db.Column('raspberry_id', db.Integer, db.ForeignKey('raspberry.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.PrimaryKeyConstraint('raspberry_id', 'user_id')
)


@dataclass
class Raspberry(db.Model, Base):
    id: int
    updateAt: datetime
    name: str

    name = db.Column(db.String, nullable=True)
    hardwares = db.relationship("Hardware", backref="raspberry", lazy='dynamic')
    users = db.relationship('User', secondary=RaspberryUser, back_populates='raspberries', lazy='joined')

    def __hash__(self):
        return hash(self.id)


class RevokedToken(db.Model):
    id: int
    jti: str
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


@dataclass
class User(db.Model, Base):
    id: int
    updateAt: datetime
    email: str
    password: str

    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    raspberries = db.relationship('Raspberry', secondary=RaspberryUser, back_populates='users', lazy='dynamic')
    @classmethod
    def post(cls, kw):
        db.session.rollback()
        kw['password'] = bcrypt.generate_password_hash(kw['password']).decode('utf-8')
        obj = cls(**kw)
        obj.updateAt = datetime.utcnow()
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def put(cls, ids, kw):
        obj = cls.query.filter_by(**ids).first_or_404()
        for k in kw:
            if k is 'password':
                kw['password'] = bcrypt.generate_password_hash(kw['password']).decode('utf-8')
                obj.__setattr__(k, kw[k])
            else:
                obj.__setattr__(k, kw[k])
        obj.updateAt = datetime.utcnow()
        db.session.commit()
        return obj

    def __hash__(self):
        return hash(self.id)
