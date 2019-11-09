from run import db
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_username(cls, username):
       return cls.query.filter_by(username = username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class RestaurantModel(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(250))
    latitude = db.Column(db.String(30))
    longitude = db.Column(db.String(30))
    locality = db.Column(db.String(100))
    cuisines = db.Column(db.String(250))
    timings = db.Column(db.String(100))
    average_cost_for_two = db.Column(db.Integer)
    aggregate_rating = db.Column(db.Float)
    votes = db.Column(db.Integer)

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'name': x.name,
                'address': x.address,
                'latitude': x.latitude,
                'longitude': x.longitude,
                'locality': x.locality,
                'cuisines': x.cuisines,
                'timings': x.timings,
                'average_cost_for_two': x.average_cost_for_two,
                'aggregate_rating': x.aggregate_rating,
                'votes': x.votes,
            }
        return {'restaurants': list(map(lambda x: to_json(x), RestaurantModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    def add(self):
        db.session.add(self)
        db.session.commit()

class HotelModel(db.Model):
    __tablename__ = 'hotels'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(250))
    latitude = db.Column(db.String(30))
    longitude = db.Column(db.String(30))
    locality = db.Column(db.String(100))
    aggregate_rating = db.Column(db.Float)
    votes = db.Column(db.Integer)

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'name': x.name,
                'address': x.address,
                'latitude': x.latitude,
                'longitude': x.longitude,
                'locality': x.locality,
                'aggregate_rating': x.aggregate_rating,
                'votes': x.votes,
            }
        return {'hotels': list(map(lambda x: to_json(x), HotelModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    def add(self):
        db.session.add(self)
        db.session.commit()

class AttractionModel(db.Model):
    __tablename__ = 'attractions'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(250))
    latitude = db.Column(db.String(30))
    longitude = db.Column(db.String(30))
    locality = db.Column(db.String(100))
    aggregate_rating = db.Column(db.Float)
    votes = db.Column(db.Integer)

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'name': x.name,
                'address': x.address,
                'latitude': x.latitude,
                'longitude': x.longitude,
                'locality': x.locality,
                'aggregate_rating': x.aggregate_rating,
                'votes': x.votes,
            }
        return {'attractions': list(map(lambda x: to_json(x), AttractionModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    def add(self):
        db.session.add(self)
        db.session.commit()

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)
