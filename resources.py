from flask import Flask, request
from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel, RestaurantModel, HotelModel, AttractionModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import json
from flask_jsonpify import jsonify
import requests
from geopy.geocoders import Nominatim

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class Home(Resource):
    def get(self):
        return "<h1>Hello World!</h1>"

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}, 303

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'], expires_delta=False)
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                # 'refresh_token': refresh_token
                }, 201
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 404

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'], expires_delta=False)
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                #'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}, 403


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }

class Planner(Resource):
    @jwt_required
    def get(self, location):
        geolocator = Nominatim(user_agent="python/flask")
        loc = geolocator.geocode(location, timeout=5000)
        coord=(loc.latitude, loc.longitude)
        hotels =  HotelModel.ranking(coord)
        for hotel in hotels["hotels"]:
            this_coord = (hotel["latitude"], hotel["longitude"])
            hotel["recreations"] = AttractionModel.ranking(this_coord)["attractions"][:10]
            hotel["restaurants"] = RestaurantModel.ranking(this_coord)["restaurants"][:10]
        return hotels

class Restaurant(Resource):
    @jwt_required
    def get(self):
        return RestaurantModel.return_all()

    @jwt_required
    def post(self):
        headers = {'user-key': '760979de1c65102782d0e922ad3fb806'}
        #url = "https://developers.zomato.com/api/v2.1/geocode?lat=-6.916055&lon=107.628391"
        url = "https://developers.zomato.com/api/v2.1/search?entity_id=11052&entity_type=city"
        response = requests.get(url, headers=headers)
        data = json.loads(response.content)
        total_result = data["results_found"];
        for i in range(0, total_result, 20):
            url = "https://developers.zomato.com/api/v2.1/search?entity_id=11052&entity_type=city&start="+str(i)
            response = requests.get(url, headers=headers)
            data = json.loads(response.content)
            for restaurant in data["restaurants"]:
                new_restaurant = RestaurantModel(
                    name = restaurant["restaurant"]["name"],
                    address = restaurant["restaurant"]["location"]["address"],
                    latitude = restaurant["restaurant"]["location"]["latitude"],
                    longitude = restaurant["restaurant"]["location"]["longitude"],
                    locality = restaurant["restaurant"]["location"]["locality"],
                    cuisines = restaurant["restaurant"]["cuisines"],
                    timings = restaurant["restaurant"]["timings"],
                    average_cost_for_two = restaurant["restaurant"]["average_cost_for_two"],
                    aggregate_rating = restaurant["restaurant"]["user_rating"]["aggregate_rating"],
                    votes = restaurant["restaurant"]["user_rating"]["votes"],
                )
                new_restaurant.add()
        return "Fetched", 201

    @jwt_required
    def delete(self):
        return RestaurantModel.delete_all()

class Hotel(Resource):
    @jwt_required
    def get(self):
        return HotelModel.return_all()

    @jwt_required
    def post(self):
        url = "http://api.tripadvisor.com/api/partner/2.0/location/297704/hotels?key=2222d03bbf2f48f9a48ca4cb9ced52a3&lang=id"
        response = requests.get(url)
        data = json.loads(response.content)
        for hotel in data["data"]:
            new_hotel = HotelModel(
                name = hotel["name"],
                address = hotel["address_obj"]["street1"],
                latitude = hotel["latitude"],
                longitude = hotel["longitude"],
                locality = hotel["address_obj"]["street2"],
                aggregate_rating = hotel["rating"],
                votes = hotel["num_reviews"],
            )
            new_hotel.add()
        return "Fetched", 201

    @jwt_required
    def delete(self):
        return HotelModel.delete_all()

class Attraction(Resource):
    @jwt_required
    def get(self):
        return AttractionModel.return_all()

    @jwt_required
    def post(self):
        url = "http://api.tripadvisor.com/api/partner/2.0/location/297704/attractions?key=2222d03bbf2f48f9a48ca4cb9ced52a3&lang=id"
        response = requests.get(url)
        data = json.loads(response.content)
        for attraction in data["data"]:
            new_attraction = AttractionModel(
                name = attraction["name"],
                address = attraction["address_obj"]["street1"],
                latitude = attraction["latitude"],
                longitude = attraction["longitude"],
                locality = attraction["address_obj"]["street2"],
                aggregate_rating = attraction["rating"],
                votes = attraction["num_reviews"],
            )
            new_attraction.add()
        return "Fetched", 201

    @jwt_required
    def delete(self):
        return AttractionModel.delete_all()
