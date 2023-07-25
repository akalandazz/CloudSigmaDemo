from sqlalchemy import func
from wh.db import db


class BeerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, server_default=func.now())
