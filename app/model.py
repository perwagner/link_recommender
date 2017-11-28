from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
