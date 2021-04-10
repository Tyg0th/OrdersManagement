from app import db, ma
from app.core.models import TimestampedModel, IsDeleted
from flask_marshmallow import fields


class Clients(IsDeleted, TimestampedModel, db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    citizenship = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)


class ClientsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Clients

    name = ma.auto_field()
    address = ma.auto_field()
    phone_number = ma.auto_field()
    citizenship = ma.auto_field()
    email = fields.fields.Email(required=True,
                                error_messages={
                                    'required': 'Email is mandatory field.',
                                    'invalid': 'The manager email is not valid.'
                                })


client_schema = ClientsSchema()
clients_schema = ClientsSchema(many=True)
