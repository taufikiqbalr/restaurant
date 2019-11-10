from run import db
from passlib.hash import pbkdf2_sha256 as sha256
from geopy.distance import distance

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

    def ranking(coord):
        def calculate():
            datas = RestaurantModel.query.all()
            for data in datas:
                this_coord = (data.latitude, data.longitude)
                dist = distance(coord, this_coord).km
                data.distance = dist
                data.distance_value = distance_value(dist)*30
                data.rating_value = data.aggregate_rating*70
                data.weight = (distance_value(dist)*30) + (data.aggregate_rating*70)
            return datas
        def to_json(x):
            return {
                'name': x.name,
                'address': x.address,
                'latitude': x.latitude,
                'longitude': x.longitude,
                'locality': x.locality,
                'aggregate_rating': x.aggregate_rating,
                'votes': x.votes,
                'distance': x.distance,
                'distance_value': x.distance_value,
                'rating_value': x.rating_value,
                'weight': x.weight,
            }
        def distance_value(x):
            if (x < 1):
                return 10
            elif (x < 1.5):
                return 8
            elif (x < 2):
                return 6
            elif (x < 3):
                return 4
            elif (x < 4):
                return 2
            else:
                return 1
        return {'restaurants': sorted(list(map(lambda x: to_json(x), calculate())), key=lambda k: k['distance'], reverse=False)}

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

    def ranking(coord):
        def calculate():
            datas = HotelModel.query.all()
            for data in datas:
                this_coord = (data.latitude, data.longitude)
                dist = distance(coord, this_coord).km
                data.distance = dist
                data.distance_value = distance_value(dist)*30
                data.rating_value = data.aggregate_rating*70
                data.weight = (distance_value(dist)*30) + (data.aggregate_rating*70)
            return datas
        def to_json(x):
            return {
                'name': x.name,
                'address': x.address,
                'latitude': x.latitude,
                'longitude': x.longitude,
                'locality': x.locality,
                'aggregate_rating': x.aggregate_rating,
                'votes': x.votes,
                'distance': x.distance,
                'distance_value': x.distance_value,
                'rating_value': x.rating_value,
                'weight': x.weight,
            }
        def distance_value(x):
            if (x < 1):
                return 10
            elif (x < 1.5):
                return 8
            elif (x < 2):
                return 6
            elif (x < 3):
                return 4
            elif (x < 4):
                return 2
            else:
                return 1
        return {'hotels': sorted(list(map(lambda x: to_json(x), calculate())), key=lambda k: k['distance'], reverse=False)}

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

    def ranking(coord):
        def calculate():
            datas = AttractionModel.query.all()
            for data in datas:
                this_coord = (data.latitude, data.longitude)
                dist = distance(coord, this_coord).km
                data.distance = dist
                data.distance_value = distance_value(dist)*30
                data.rating_value = data.aggregate_rating*70
                data.weight = (distance_value(dist)*30) + (data.aggregate_rating*70)
            return datas
        def to_json(x):
            return {
                'name': x.name,
                'address': x.address,
                'latitude': x.latitude,
                'longitude': x.longitude,
                'locality': x.locality,
                'aggregate_rating': x.aggregate_rating,
                'votes': x.votes,
                'distance': x.distance,
                'distance_value': x.distance_value,
                'rating_value': x.rating_value,
                'weight': x.weight,
            }
        def distance_value(x):
            if (x < 1):
                return 10
            elif (x < 1.5):
                return 8
            elif (x < 2):
                return 6
            elif (x < 3):
                return 4
            elif (x < 4):
                return 2
            else:
                return 1
        return {'attractions': sorted(list(map(lambda x: to_json(x), calculate())), key=lambda k: k['distance'], reverse=False)}

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
