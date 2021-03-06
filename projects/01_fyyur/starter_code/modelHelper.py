from datetime import datetime
from models import db, Artist, Venue, Shows
import pprint


def getStructureData(venue=None, artist=None):

    d = {
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }
    if venue:
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
        genres = venue.genres
        # add new keys
        venue = venue.__dict__
        venue.update(d)

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
        venue["genres"] = genres
        venue["upcoming_shows_count"] = len(upcoming_shows)

        pprint.pprint(venue)
        return venue
    elif artist:
        pastShows = db.session.query(
            Shows.venue_id,
            Shows.start_time).filter(
            Shows.artist_id == artist.id,
            Shows.start_time < datetime.now()
        ).all()
        upcoming_shows = db.session.query(
            Shows.venue_id,
            Shows.start_time).filter(
            Shows.artist_id == artist.id,
            Shows.start_time > datetime.now()
        ).all()
        # add new keys
        artist = artist.__dict__
        artist.update(d)

        if len(pastShows) != 0:
            for show in pastShows:

                venue_id = show.venue_id
                start_time = datetime.strftime(
                    show.start_time, '%Y-%m-%d %H:%M:%S')

                venue_info = db.session.query(
                    Venue.id,
                    Venue.name,
                    Venue.image_link).filter(Venue.id == venue_id).all()

                for ele in venue_info:
                    artist["past_shows"].append({
                        "venue_id": ele[0],
                        "venue_name": ele[1],
                        "venue_image_link": ele[2],
                        "start_time": start_time
                    })

        artist["past_shows_count"] = len(pastShows)

        if len(upcoming_shows) != 0:
            for show in upcoming_shows:

                venue_id = show.venue_id
                start_time = datetime.strftime(
                    show.start_time, '%Y-%m-%d %H:%M:%S')

                venue_info = db.session.query(
                    Venue.id,
                    Venue.name,
                    Venue.image_link).filter(Venue.id == venue_id).all()

                for ele in venue_info:
                    artist["upcoming_shows"].append({
                        "venue_id": ele[0],
                        "venue_name": ele[1],
                        "venue_image_link": ele[2],
                        "start_time": start_time
                    })

        artist["upcoming_shows_count"] = len(upcoming_shows)
        return artist