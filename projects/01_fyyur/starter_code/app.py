#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import pprint
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import db, Artist, Venue, Shows
from modelData import artistData, venueData, showData
from datetime import datetime

from modelData import row2dict
from modelHelper import getStructureData
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Backfill the data to the models;
#----------------------------------------------------------------------------#
with app.app_context():

    if Venue.query.count() == 0:
        print("Adding venue data!")
        newEntries = []
        for data in venueData:
            newData = Venue(**data)
            newEntries.append(newData)
        db.session.add_all(newEntries)
        db.session.commit()
        db.session.close()

    if Artist.query.count() == 0:
        print("Adding the data")
        for data in artistData:
            db.session.add(Artist(**data))
        db.session.commit()
        db.session.close()

    if Shows.query.count() == 0:
        print("Adding show data!")
        for data in showData:
            db.session.add(Shows(**data))
        db.session.commit()
        db.session.close()
    print("Data All Set!")


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    allVenues = [
        {
            "city": "San Francisco",
            "state": "CA",
            "venues": []
        },
        {
            "city": "New York",
            "state": "NY",
            "venues": []
        }
    ]
    newData = db.session.query(Venue.id, Venue.name, Venue.city, Venue.state, Shows.id.label(
        'show_id'), Shows.start_time).outerjoin(Shows)
    # venueSF = db.session.query(Venue).filter(Venue.state == 'CA').all()
    # venueNY = db.session.query(Venue).filter(Venue.state == 'NY').all()
    venueSF = newData.filter(Venue.state == 'CA').all()
    venueNY = newData.filter(Venue.state == 'NY').all()

    sfvenues = {}
    for venue in venueSF:
        showDate = datetime.strftime(venue.start_time, '%Y-%m-%d %H:%M:%S')
        if venue.id in sfvenues and showDate > current_time:
            sfvenues[venue.id] = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": sfvenues[venue.id]["num_upcoming_shows"]
            }
            sfvenues[venue.id]["num_upcoming_shows"] += 1
        elif venue.id not in sfvenues and showDate > current_time:
            sfvenues[venue.id] = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": 1
            }
        elif venue.id not in sfvenues and showDate < current_time:
            sfvenues[venue.id] = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": 0
            }
        else:
            sfvenues[venue.id] = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": sfvenues[venue.id]["num_upcoming_shows"]
            }

    nyvenues = {}
    for venue in venueNY:
        showDate = datetime.strftime(
            venue.start_time, '%Y-%m-%d %H:%M:%S') if venue.show_id is not None else 0
        if venue.show_id == None:
            nyvenues[venue.id] = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": 0
            }
        elif venue.id in nyvenues and showDate > current_time:
            nyvenues[venue.id] = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": nyvenues[venue.id]["num_upcoming_shows"]
            }
            nyvenues[venue.id]["num_upcoming_shows"] += 1
        elif venue.id not in nyvenues and showDate > current_time:
            nyvenues[venue.id] = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": 1
            }
        elif venue.id not in nyvenues and showDate < current_time:
            nyvenues[venue.id] = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": 0
            }
        else:
            nyvenues[venue.id] = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": nyvenues[venue.id]["num_upcoming_shows"]
            }
        for value in nyvenues.values():
            allVenues[1]['venues'].append(value)
        for value in sfvenues.values():
            allVenues[0]['venues'].append(value)

    return render_template('pages/venues.html', areas=allVenues)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = "%{}%".format(request.form.get('search_term'))
    matchVenues = db.session.query(
        Venue.id,
        Venue.name,
        Venue.state).filter(Venue.name.ilike(search_term)).all()

    newresponse = {
        "count": len(matchVenues),
        "data": []
    }

    if matchVenues:
        for venue in matchVenues:
            name = db.session.query(Venue.name).filter(
                Venue.id == venue.id).all()
            upcoming_shows = db.session.query(
                Shows.venue_id,
                Shows.start_time).filter(
                    Shows.venue_id == venue.id,
                    Shows.start_time > datetime.now()
            ).all()
            num_upcoming_shows = len(upcoming_shows)
            newresponse['data'].append({
                "id": venue.id,
                "name": name,
                "num_upcoming_shows": num_upcoming_shows
            })
    return render_template('pages/search_venues.html', results=newresponse, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
    print("The id should be: ", venue_id)
    allVenues = db.session.query(Venue).filter(Venue.id == venue_id).all()
    transVenuesData = []
    for venue in allVenues:
        # finally append the venue to a list
        transVenuesData.append(getStructureData(venue, artist=None))

    pprint.pprint(transVenuesData[0])
    data = list(filter(lambda d: d['id'] ==
                       venue_id, transVenuesData))[0]
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # DONE: insert form data as a new Venue record in the db, instead
    # DONE: modify data to be the data object returned from db insertion

    # TODO: fix the error when creating a new venue: there willl be exixting venues duplicated,
    # and it cannot show new venues which not belong to NY & SF.
    error = False
    try:
        formdata = request.form.to_dict()
        formdata['genres'] = request.form.getlist('genres')
        print(formdata)
        db.session.add(Venue(**formdata))
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        error = True
        print(e)
    finally:
        db.session.close()
        if error:
            flash('An error occured. Venue ' +
                  request.form['name'] + ' Could not be listed!')
        else:
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # Done: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False

    try:
        venue = Venue.query.get(venue_id)
        name = venue.name
        db.session.delete(venue)
        db.session.commit()
    except Exception as e:
        error = True
        print(f"The error is {e}")
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            flash(
                f"An error has occured. Venue {venue_id} could not be deleted!")
            abort(400)
        else:
            flash(f"The venue {venue_id}: {name} has deleted!")
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # DONE: replace with real data returned from querying the database
    artists = db.session.query(Artist).all()
    newData = []
    for artist in artists:
        newData.append({
            "id": artist.id,
            "name": artist.name
        })
    return render_template('pages/artists.html', artists=newData)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    # "%{}%".format(request.form.get('search_term'))
    search_term = "%{}%".format(request.form.get('search_term'))

    searched_artist = db.session.query(Artist).filter(
        Artist.name.ilike(search_term)).all()
    num_searched_artist = len(searched_artist)
    newData = {
        "count": num_searched_artist,
        "data": []
    }
    for artist in searched_artist:
        upcoming_ones = Shows.query.filter(
            artist.id == Shows.artist_id, Shows.start_time > datetime.now()).all()
        num_coming = len(upcoming_ones)
        if(num_coming > 0):
            newData["data"].append({
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": num_coming
            })
        else:
            newData["data"].append({
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": 0
            })
    #pprint.pprint(newData)
    return render_template('pages/search_artists.html', results=newData, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    try:
        artistInfo = db.session.query(Artist).filter(Artist.id == artist_id).all()
        transArtistData = []
        for artist in artistInfo:
            transArtistData.append(getStructureData(venue = None, artist = artist))

        data = list(filter(lambda d: d['id'] ==
                        artist_id, transArtistData))[0]
        return render_template('pages/show_artist.html', artist=data)
    except Exception as e:
        flash(f"Error...Cannot find the artist you are looking for!")
        return redirect(url_for('artists'))
    

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artistInfo = Artist.query.filter_by(id=artist_id).first()
    form = ArtistForm()
    # Done: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artistInfo)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # DONE: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    try:
        form = ArtistForm()
        artist = Artist.query.get(artist_id)

        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = form.genres.data
        artist.facebook_link = form.facebook_link.data
        db.session.commit()
        flash(f"The data has been updated!")
        return redirect(url_for('show_artist', artist_id=artist_id))
    except Exception as e:
        db.session.rollback()
        flash(f"Error has occured when update the artist:{artist.name}")
        print(e)
        return redirect(url_for('show_artist', artist_id=artist_id))
    finally:
        db.session.close()

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venueInfo = Venue.query.get(venue_id)
    # DONE: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venueInfo)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # DONE: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    try:
        form = VenueForm()
        venueInfo = Venue.query.get(venue_id)
        venueInfo.city = form.city.data
        venueInfo.state = form.state.data
        venueInfo.address = form.address.data
        venueInfo.phone = form.phone.data
        venueInfo.genres = form.genres.data
        venueInfo.facebook_link = form.facebook_link.data
        db.session.commit()
        flash(f"The venue data has been updated!")
        return redirect(url_for('show_venue', venue_id=venue_id))
    except Exception as e:
        db.session.rollback()
        print(e)
        flash(f"Error occurred...The update for venue: {venueInfo.name} failed")
        return redirect(url_for('show_venue', venue_id=venue_id))
    finally:
        db.session.close()
#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)
# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
