from extensions import db
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class Specification(db.Model):
    __tablename__ = "specifications"
    id = db.Column(db.Integer, primary_key=True)
    system = db.Column(db.String(250), nullable=False)
    support_name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    number_of_supports = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "posts" refers to the posts property in the User class.
    author = relationship("User", back_populates="spec")
    status = db.Column(db.String(250), nullable=False)
    object = db.Column(db.String(250))
    object_address = db.Column(db.String(250))
    send_date = db.Column(db.String(250))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    company = db.Column(db.String(1000))
    spec = relationship("Specification", back_populates="author")
    is_authenticated = UserMixin


class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100))
    message = db.Column(db.String(1500), nullable=False)
    date = db.Column(db.String(250), nullable=False)