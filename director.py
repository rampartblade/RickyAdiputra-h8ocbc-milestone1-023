from flask import make_response, abort
from config import db
from models import *

def read_all(): #get all data
    """
    This function responds to a request for /api/director
    with the complete lists of director movie

    :return:        json string of list of director movie
    """

    director_item = Directors.query.order_by(Directors.id).limit(10)  #.all() ==> untuk mengambil semua data, diganti limit untuk sementara karena data yang diambil terlalu banyak
    director_Schema = DirectorsSchema(many=True)
    data = director_Schema.dump(director_item)
    
    if len(data) == 0:
        return abort(404,f"Database empty")
    
    return data

def read_one(id): #get 1 data
    """
    This function responds to a request for /api/director/{id}
    with one matching director from database

    :param id:          Id of director to find
    :return:            person matching id
    """

    director_item = Directors.query.filter(Directors.id == id).one_or_none()

    if director_item is not None:
        director_Schema = DirectorsSchema()
        data = director_Schema.dump(director_item)
        return data

    else:
        abort(404, f"Director Id: {id} Not Found")

def read_one_name(director_name): # read one data
    """
    This function responds to a request for
    /api/director/{director_id}/movie/{movie_id}
    with one matching movie for the associated director by id

    :param director_id:       Id of director the movie is related to
    :param movie_id:         Id of the movie
    :return:                json string of note contents
    """
    director = Directors.query.filter(Directors.name.like(f'%{director_name}%')).all()

    if director is not None:
        director_Schema = DirectorsSchema(many=True)
        data = director_Schema.dump(director)

        if len(data) == 0:
            return abort(404,f"Director with name : {director_name} was not found")
        return data

    else:
        abort(404, f"Director name : {director_name} was not found")

def create(director): #post data
    """
    This function creates a new director 
    based on the passed in director data

    :param director:  director to create in director structure
    :return:        201 on success and data
    """
    department = director.get("department")
    gender = director.get("gender")
    name = director.get("name")
    uid = director.get("uid")

    if department is None or department is '':
        abort(409, 'field department is invalid or required')
    if gender is None:
        abort(409, 'field gender is invalid or required')
    if name is None or name is '':
        abort(409, 'field name is invalid or required')
    if uid is None or uid is 0:
        abort(409, 'field uid is invalid or required')


    #director_Schema = DirectorsPostSchema()
    #new_director = director_Schema.load(existing_director, session=db.session)
    director_Schema = DirectorsPostSchema()
    new_director = director_Schema.load(director, session=db.session)

    db.session.add(new_director)
    db.session.commit()

    data = director_Schema.dump(new_director)

    return data,201
    

def update(id, director): #update data
    """
    This function updates an existing director in director structure

    :param id:          Id of the director to update in director structure
    :param person:      director to update
    :return:            updated director structure
    """

    department = director.get("department")
    gender = director.get("gender")
    name = director.get("name")
    uid = director.get("uid")

    if department is None or department is '':
        abort(409, 'field department is invalid or required')
    if gender is None or gender is 0:
        abort(409, 'field gender is invalid or required')
    if name is None or name is '':
        abort(409, 'field name is invalid or required')
    if uid is None or uid is 0:
        abort(409, 'field uid is invalid or required')


    update_director = Directors.query.filter(Directors.id == id).one_or_none()

    if update_director is not None:

        director_Schema = DirectorsPostSchema()
        update = director_Schema.load(director, session = db.session)

        update.id = id
        db.session.merge(update)
        db.session.commit()

        data = director_Schema.dump(update)

        return data, 200

    else:
        abort(404, f"Director Id: {id} Not Found")

def delete(id):
    """
    This function deletes a director from director structure

    :param id:   Id of the director to delete
    :return:            200 on successful delete, 404 if not found
    """
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