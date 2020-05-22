artistData = [
    {
        "id": 4,
        "name": "Guns N Petals",
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "genres": ["Rock n Roll"],
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "website": "https://www.gunsnpetalsband.com",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!"
    },
    {
        "id": 5,
        "name": "Matt Quevedo",
        "city": "New York",
        "state": "NY",
        "phone": "300-400-5000",
        "genres": ["Jazz"],
        "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "facebook_link": "https://www.facebook.com/mattquevedo923251523",
        "seeking_venue": False
    },
    {
        "id": 6,
        "name": "The Wild Sax Band",
        "city": "San Francisco",
        "state": "CA",
        "phone": "432-325-5432",
        "genres": ["Jazz", "Classical"],
        "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "seeking_venue": False
    }]


venueData = [
    {
        "id": 1,
        "name": "The Musical Hop",
        "city": "San Francisco",
        "state": "CA",
        "address": "1015 Folsom Street",
        "phone": "123-123-1234",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "website": "https://www.themusicalhop.com",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us."
    },
    {
        "id": 2,
        "name": "The Dueling Pianos Bar",
        "city": "New York",
        "state": "NY",
        "address": "335 Delancey Street",
        "phone": "914-003-1132",
        "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        "facebook_link": "https://www.facebook.com/theduelingpianos",
        "genres": ["Classical", "R&B", "Hip-Hop"],
        "website": "https://www.theduelingpianos.com",
        "seeking_talent": False,
    },
    {
        "id": 3,
        "name": "Park Square Live Music & Coffee",
        "city": "San Francisco",
        "state": "CA",
        "address": "34 Whiskey Moore Ave",
        "phone": "415-000-1234",
        "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
        "website": "https://www.parksquarelivemusicandcoffee.com",
        "seeking_talent": False

    }
]

showData = [
    {
        "venue_id": 1,
        "artist_id": 4,
        "start_time": "2019-05-21T21:30:00.000Z"
    },
    {
        "venue_id": 3,
        "artist_id": 5,
        "start_time": "2019-06-15T23:00:00.000Z"
    },
    {
        "venue_id": 3,
        "artist_id": 6,
        "start_time": "2035-04-01T20:00:00.000Z"
    },
    {
        "venue_id": 3,
        "artist_id": 6,
        "start_time": "2035-04-08T20:00:00.000Z"
    },
    {
        "venue_id": 3,
        "artist_id": 6,
        "start_time": "2035-04-15T20:00:00.000Z"
    }
]

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d