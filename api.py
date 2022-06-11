from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource
from flask_cors import CORS
from utils import *


app = Flask(__name__)
api = Api(app=app)
cors = CORS(app, resources={r"/v1/*":{"origins":"*"}})

parser = reqparse.RequestParser()
parser.add_argument('date_published', type=str, help='Date when the temperature was recorded')
parser.add_argument('average_temperature', type=float, help='Average temperature of the city')
parser.add_argument('average_temperature_uncertainty', type=float, help='Average temperature of the city')
parser.add_argument('city', type=str, help='city where the temperature was recorded')
parser.add_argument('country', type=str, help='country where the temperature was recorded')
parser.add_argument('latitude', type=str, help='latitude of the temperature ')
parser.add_argument('longitude', type=str, help='longitude of the temperature ')
parser.add_argument('year', type=int, help='Year when the temperature was recorded')
parser.add_argument('start', type=str, help='Start Date when the temperature was recorded')
parser.add_argument('end', type=str, help='End Date when the temperature was recorded')
parser.add_argument('correction', type=float, help='End Date when the temperature was recorded')


class Climate(Resource):

    def get(self):
        args = parser.parse_args()
        if args.start and args.end:
            records = get_item_by_monthly(args.start, args.end)
            return send_response(records)

        if args.year:
            result = get_item_by_year(args.year)
            return send_response(result)

    def post(self):

        args = parser.parse_args()
        create_item(args)
        return {
            "status": "Successfully inserted the row"
        }

    def put(self):
        args = parser.parse_args()

        if args.average_temperature and args.average_temperature_uncertainty:
            update_item_by_city_and_date(args)
            return {
                "status": "Successfully updated the row"
            }

        if args.correction and args.year:
            update_item_by_year(args)
            return {"status": "Successfully updated the row"}


api.add_resource(Climate, '/v1/city')


def send_response(result):
    if isinstance(result, Instance):
        return jsonify({"date": result.date_published, "avg_temperature": result.average_temperature,
                        "city": result.city, "country": result.country})

    return jsonify([{"date": i.date_published, "avg_temperature": i.average_temperature, "city": i.city,
                     "country": i.country} for i in result])


if __name__ == '__main__':
    app.run(debug=True)