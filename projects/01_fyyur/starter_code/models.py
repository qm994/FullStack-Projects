from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), nullable = False, default = False)
    seeking_description = db.Column(db.String(500))

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(), nullable = True, default = False)
    seeking_description = db.Column(db.String(500))

    def __repr__(self):
        return f'<Artist {self.id} {self.name} >'

class Shows(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=True)
    start_time = db.Column(db.DateTime(), nullable=True)

    def __repr__(self):
        return f'<Shows {self.id} {self.artist_id} {self.venue_id}>'