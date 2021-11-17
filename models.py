from datetime import datetime
from os import name
from config import db, ma
from marshmallow import fields

class Directors(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    gender = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    department = db.Column(db.Text)
    movies = db.relationship(
        'Movies',
        backref='directors',
        cascade = 'all, delete, delete-orphan',
        single_parent = True,
        order_by = 'asc(Movies.id)'
    )

class Movies(db.Model):
    __tablename__ = 'movies'
    #avocado_id = db.Column()
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.Text)
    budget = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.Text)
    revenue = db.Column(db.Integer)
    title = db.Column(db.Text)
    vote_average = db.Column(db.REAL)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.Text)
    tagline = db.Column(db.Text)
    uid = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))

class DirectorsSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    class Meta:
        model = Directors
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        #unknown = EXCLUDE

    movies = fields.Nested('DirectorsMoviesSchema', default=[], many=True)

class MoviesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movies
        sqla_session = db.session    
        load_instance = True
        include_relationships = True
       #unknown = EXCLUDE
    
    directors = fields.Nested('MoviesDirectorsSchema', default=None)

class DirectorsMoviesSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    budget = fields.Int()
    director_id = fields.Int()
    original_title = fields.Str()
    overview = fields.Str()
    popularity = fields.Str()
    release_date = fields.Str()
    revenue = fields.Int()
    tagline = fields.Str()
    title = fields.Str()
    uid = fields.Int()
    vote_average = fields.Number()
    vote_count = fields.Int()

class MoviesDirectorsSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    department = fields.Str()
    gender = fields.Int()
    name = fields.Str()
    uid = fields.Int()


