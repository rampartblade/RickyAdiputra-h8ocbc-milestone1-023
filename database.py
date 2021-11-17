import os
#from datetime import datetime
from config import db
from models import Directors, Movies

DIRECTORS = [
  {
    "department": "string",
    "gender": 0,
    "id": 0,
    "movies": [
      {
        "budget": 0,
        "director_id": 0,
        "id": 0,
        "original_title": "string",
        "overview": "string",
        "popularity": 0,
        "release_date": "string",
        "revenue": 0,
        "tagline": "string",
        "title": "string",
        "uid": 0,
        "vote_average": 0,
        "vote_count": 0
      }
    ],
    "name": "string",
    "uid": 0
  }
]

if os.path.exists('final_proj_pk.db'):
    os.remove('final_proj_pk.db')

db.create_all()

for director in DIRECTORS:
    dire = Directors(
        department = director['department'],
        gender = director['gender'],
        name = director['name'],
        uid = director['uid']        
    )

    for m in director['movies']:
        dire.movies.append(
            Movies(
                budget = m['budget'],
                director_id = m['director_id'],
                original_title = m['original_title'],
                overview = m['overview'],
                popularity = m['popularity'],
                release_date = m['release_date'],
                revenue = m ['revenue'],
                tagline = m ['tagline'],
                title = m ['title'],
                uid = m ['uid'],
                vote_average = m ['vote_average'],
                vote_count = m ['vote_count']
            )
        )
    db.session.add(dire)

db.session.commit()
