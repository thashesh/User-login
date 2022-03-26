
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Models
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    profile = db.Column(db.String, nullable=True)

    def __repr__(self):
        return "<User(name={self.first_name!r} {self.last_name!r})>".format(self=self)
    
    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()