from flask import Flask
from flask_restful import reqparse, Api, Resource
from flask_cors import CORS
from climate_api.utils import *


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
        try:

            args = parser.parse_args()
            if args.start and args.end:
                records = get_item_by_monthly(args.start, args.end)
                return send_response(records), 200

            if args.year:
                result = get_item_by_year(args.year)
                return send_response(result), 200
        except Exception as e:
            return CustomResponse("Error in fetching the record", 500).body, 500

    def post(self):
        try:
            args = parser.parse_args()
            if args.correction and args.year:
                create_item_by_condition(args.year, args.correction)
                return CustomResponse("Successfully inserted the row", 201).body, 201
            create_item(args)
            return CustomResponse("Successfully inserted the row", 201).body, 201
        except Exception as e:
            return CustomResponse("Error in creation of record", 500).body

    def put(self):
        try:
            args = parser.parse_args()

            if args.average_temperature and args.average_temperature_uncertainty:
                update_item_by_city_and_date(args)
                return CustomResponse("Successfully updated the row", 200).body,200

            if args.correction and args.year:
                update_item_by_year(args)
                return CustomResponse("Successfully updated the row", 200).body, 200
        except Exception as e:
            return CustomResponse("Error in updating the record", 500).body, 500


api.add_resource(Climate, '/v1/city')


def send_response(result):
    if isinstance(result, Instance):
        return ({"date": str(result.date_published), "avg_temperature": result.average_temperature,
                 "average_temperature_uncertainty": result.average_temperature_uncertainty, "city": result.city,
                 "country": result.country})

    return ([{"date": str(i.date_published), "avg_temperature": i.average_temperature, "average_temperature_uncertainty": i.average_temperature_uncertainty,
              "city": i.city, "country": i.country} for i in result])


if __name__ == '__main__':
    app.run(debug=True)