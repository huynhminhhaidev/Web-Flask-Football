from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    fullname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True)
    phonenumber = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    birthday = db.Column(db.String(255))
    role = db.Column(db.String(255))
    password = db.Column(db.String(255))
    linkFB = db.Column(db.String(255))
    # date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, fullname, gender, birthday, phonenumber, email, role, password, linkFB):
        self.fullname = fullname
        self.email = email
        self.phonenumber = phonenumber
        self.gender = gender
        self.birthday = birthday
        self.role = role
        self.password = password
        self.linkFB = linkFB

class Address(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    idHost = db.Column(db.Integer(), db.ForeignKey('user.id'))
    name = db.Column(db.String(255))
    address = db.Column(db.String(255), unique = True)
    city = db.Column(db.String(255))
    district = db.Column(db.String(255))
    linkAddress = db.Column(db.String(255))
    iframe = db.Column(db.String(500))
    phone1 = db.Column(db.String(255))
    phone2 = db.Column(db.String(255))
    service = db.Column(db.String(255))
    note = db.Column(db.String(255))

    def __init__(self, idHost, name, address, city, district, linkAddress, iframe, phone1, phone2, service, note):
        self.idHost = idHost
        self.name = name
        self.address = address
        self.city = city
        self.district = district
        self.linkAddress = linkAddress
        self.iframe = iframe
        self.phone1 = phone1
        self.phone2 = phone2
        self.service = service
        self.note = note

class Pitch(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    idAddress = db.Column(db.Integer(), db.ForeignKey('address.id'))
    idHost = db.Column(db.Integer(), db.ForeignKey('user.id'))
    name = db.Column(db.String(255))
    kind = db.Column(db.String(255))

    def __init__(self, idAddress, idHost, name, kind):
        self.idAddress = idAddress
        self.idHost = idHost
        self.name = name
        self.kind = kind

class Time(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    idPitch = db.Column(db.Integer(), db.ForeignKey('pitch.id'))
    timeS = db.Column(db.String(255))
    timeE = db.Column(db.String(255))
    cost = db.Column(db.String(255))

    def __init__(self, idPitch, timeS, timeE, cost):
        self.idPitch = idPitch
        self.timeS = timeS
        self.timeE = timeE
        self.cost = cost

class Matchh(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    idTime = db.Column(db.Integer(), db.ForeignKey('time.id'))
    idMember = db.Column(db.Integer(), db.ForeignKey('user.id'))
    idPitch = db.Column(db.Integer(), db.ForeignKey('pitch.id'))
    idAddress = db.Column(db.Integer(), db.ForeignKey('address.id'))
    date = db.Column(db.String(255))
    phonebackup = db.Column(db.String(255))
    note = db.Column(db.String(255))
    status = db.Column(db.String(255))
    datetimePay = db.Column(db.String(255))
    statusPay = db.Column(db.String(255))

    def __init__(self, idTime, idMember, idPitch, idAddress, date, phonebackup, note, status, datetimePay, statusPay):
        self.idTime = idTime
        self.idMember = idMember
        self.idPitch = idPitch
        self.idAddress = idAddress
        self.date = date
        self.phonebackup = phonebackup
        self.note = note
        self.status = status
        self.datetimePay = datetimePay
        self.statusPay = statusPay

class City(db.Model):
    id = db.Column(db.String(5), primary_key = True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(30))

    def __init__(self, name, type):
        self.name = name
        self.type = type

class District(db.Model):
    id = db.Column(db.String(5), primary_key = True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(30))
    idCity = db.Column(db.String(5), db.ForeignKey('city.id'))

    def __init__(self, name, type, idCity):
        self.name = name
        self.type = type
        self.idCity = idCity

class Bill(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    idMember = db.Column(db.Integer(), db.ForeignKey('user.id'))
    idMatch = db.Column(db.Integer(), db.ForeignKey('matchh.id'))
    cost = db.Column(db.String(255))

    def __init__(self, idMember, idMatch, cost):
        self.idMember = idMember
        self.idMatch = idMatch
        self.cost = cost