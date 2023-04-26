from datetime import datetime

from config import get_app_config
from marshmallow_sqlalchemy import fields

db = get_app_config().db
ma = get_app_config().ma


class Chore(db.Model):
    __tablename__ = "chore"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(128))
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    due_date = db.Column(db.DateTime, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class ChoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chore
        load_instance = True
        sqla_session = db.session


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    chores = db.relationship(Chore, backref="user")


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

    chores = fields.Nested("ChoreSchema", many=True)


chores_schema = ChoreSchema(many=True)
chore_schema = ChoreSchema()
user_schema = UserSchema()
