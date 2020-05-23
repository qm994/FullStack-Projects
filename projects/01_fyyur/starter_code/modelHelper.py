from datetime import datetime
from models import db, Artist, Venue, Shows
import pprint


def getStructureVenue(venue):
    d = {
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }
    pastShows = db.session.query(
        Shows.artist_id,
        Shows.start_time).filter(
        Shows.venue_id == venue.id,
        Shows.start_time < datetime.now()
    ).all()

    upcoming_shows = db.session.query(
        Shows.artist_id,
        Shows.start_time).filter(
        Shows.venue_id == venue.id,
        Shows.start_time > datetime.now()
    ).all()

    # add new keys
    venue = venue.__dict__
    venue.update(d)
    #venue["genres"] = list(venue["genres"])
    # add values if there are past/coming shows
    if len(pastShows) != 0:
        for show in pastShows:

            artist_id = show.artist_id
            start_time = datetime.strftime(
                show.start_time, '%Y-%m-%d %H:%M:%S')

            artist_info = db.session.query(
                Artist.id,
                Artist.name,
                Artist.image_link).filter(Artist.id == artist_id).all()

            for ele in artist_info:
                venue["past_shows"].append({
                    "artist_id": ele[0],
                    "artist_name": ele[1],
                    "artist_image_link": ele[2],
                    "start_time": start_time
                })

        venue["past_shows_count"] = len(pastShows)

    if len(upcoming_shows) != 0:
        for show in upcoming_shows:

            artist_id = show.artist_id
            start_time = datetime.strftime(
                show.start_time, '%Y-%m-%d %H:%M:%S')

            artist_info = db.session.query(
                Artist.id,
                Artist.name,
                Artist.image_link).filter(Artist.id == artist_id).all()

            for ele in artist_info:
                venue["upcoming_shows"].append({
                    "artist_id": ele[0],
                    "artist_name": ele[1],
                    "artist_image_link": ele[2],
                    "start_time": start_time
                })

        venue["upcoming_shows_count"] = len(upcoming_shows)
    
    return venue
