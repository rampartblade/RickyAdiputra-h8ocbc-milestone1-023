from flask import make_response, abort
from config import db
from models import Directors, Movies, DirectorsSchema

def read_all(): #get all data
    director_item = Directors.query.order_by(Directors.id).limit(10)  #.all() ==> untuk mengambil semua data, diganti limit untuk sementara karena data yang diambil terlalu banyak
    director_Schema = DirectorsSchema(many=True)
    data = director_Schema.dump(director_item)
    return data

def read_one(id): #get 1 data
    director_item = Directors.query.filter(Directors.id == id).one_or_none()

    if director_item is not None:
        director_Schema = DirectorsSchema()
        data = director_Schema.dump(director_item)
        return data

def create(director): #post data
    id = director.get("id")
    name = director.get("name")

    existing_id = {
        Directors.query.filter(Directors.id == id).one_or_none()
    }

    if existing_id is None:
        director_Schema = DirectorsSchema()
        new_director = director_Schema.load(director, session=db.session)

        db.session.add(new_director)
        db.session.commit()

        data = director_Schema.dump(new_director)

        return data,201
    else:
        abort(409, f"Directors {name} exists already")

def update(id, director): #update data
    update_director = Directors.query.filter(Directors.id == id).one_or_none()

    if update_director is not None:

        director_Schema = DirectorsSchema()
        update = director_Schema.load(director, session = db.session)

        db.session.merge(update)
        db.session.commit()

        data = director_Schema.dump(update_director)

        return data, 200

    else:
        abort(404, f"Director Id: {id} Not Found")

def delete(id):
    delete_director = Directors.query.filter(Directors.id == id).one_or_none()

    if delete_director is not None:
        db.session.delete(delete_director)
        db.session.commit()
        return make_response(
            f"Director with id {id} has been deleted", 200
        )

    else:
        abort(
            404,
            f"Director id : {id} not found",
        )