import datetime

from flask_sqlalchemy   import SQLAlchemy

db = SQLAlchemy(session_options={'autocommit' : False})

class Users(db.Model):
    __tablename__   = "users"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    uid         = db.Column(db.String(128), nullable=False)
    email       = db.Column(db.String(128))
    password    = db.Column(db.String(256), nullable=False)
    

class Configs(db.Model):
    __tablename__   = "configs"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer, primary_key=True)
    key         = db.Column(db.String(128))
    value       = db.Column(db.String(256))


class Hosts(db.Model):
    __tablename__   = "hosts"
    __table_args__  = {'mysql_collate' : "utf8_general_ci"}

    # Core Attributes
    idx         = db.Column(db.Integer,     primary_key=True)
    name        = db.Column(db.String(128))
    mac         = db.Column(db.String(64),  nullable=False)
    ip          = db.Column(db.String(64),  nullable=False)
    broadcast   = db.Column(db.Boolean,     default=False)
