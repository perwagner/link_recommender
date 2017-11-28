from factory import Sequence, LazyFunction, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyDecimal, FuzzyText, FuzzyInteger
from faker import Faker

from .model import User, Product, Order, db


fake = Faker(locale='en_US')


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        entity = model_class(*args, **kwargs)
        db.session.add(entity)
        db.session.commit()
        return entity

    username = LazyFunction(fake.name)
    email = FuzzyText(length=12)


class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = db.session

    name = fake.name()
    price = FuzzyDecimal(0.5, 100.7)


class OrderFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Order
        sqlalchemy_session = db.session

    customer = SubFactory(UserFactory)
    product = SubFactory(ProductFactory)