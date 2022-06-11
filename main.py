import flask, requests, json
from flask import request, jsonify,  Response
from mysql import connector
from db_utils import connect_db
from datetime import datetime
import mysql.connector


# The flask app for serving predictions
app = flask.Flask(__name__)


def showMessage(message):
    respone = jsonify(message)
    respone.status_code = 404
    return respone


@app.route('/create', methods=['POST'])
def add_temperature():
    try:
        data = request.json
        print(data)
        date = data['date']
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        avg_temperature = data['avg_temperature']
        avg_temperature_uncertainty = data['avg_temperature_uncertainty']
        city = data['city']
        country = data['country']
        latitude = data['latitude']
        longitude = data['longitude']

        if date and city and country and avg_temperature and request.method == 'POST':

            connection = mysql.connector.connect(host='localhost',
                                                 database='climate',
                                                 user='root',
                                                 password='root123')
            cursor = connection.cursor()
            sqlQuery = "INSERT INTO climate.global_city_temperature (date_published,average_temperature,average_temperature_uncertainty,city,country,latitude,longitude) VALUES(%s, %s, %s, %s, %s, %s, %s )"
            bindData = (date_obj, avg_temperature, avg_temperature_uncertainty, city, country, latitude, longitude)
            cursor.execute(sqlQuery, bindData)
            connection.commit()
            response = jsonify('Temperature added successfully!')
            response.status_code = 200
            return response
        else:
            return showMessage("Invalid Data")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


@app.route('/update', methods=['PUT'])
def update_temperature():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='climate',
                                       user='root',
                                       password='root123')
        cursor = conn.cursor()
        data = request.json
        date = data['date']
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        avg_temperature = data['avg_temperature']
        avg_temperature_uncertainty = data['avg_temperature_uncertainty']
        city = data['city']
        update_user_cmd = """update climate.global_city_temperature 
                             set average_temperature=%s, average_temperature_uncertainty=%s
                             where city=%s and date_published=%s"""
        cursor.execute(update_user_cmd, (avg_temperature, avg_temperature_uncertainty, city, date_obj))
        conn.commit()
        response = jsonify('User updated successfully.')
        response.status_code = 200
        return (response)
    except Exception as e:
        print(e)
        response = jsonify('Failed to update temperature.')
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()


@app.route('/city/monthly', methods=['GET'])
def get_highest_temperature_monthly():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='climate',
                                       user='root',
                                       password='root123')
        cursor = conn.cursor()
        start_date = request.args['start']
        end_date = request.args['end']
        print(start_date,end_date)
        # date = data['date']
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        update_user_cmd = """SELECT g.* FROM global_city_temperature g,
        (SELECT date_published, MAX(average_temperature) AS highest_temperature
        FROM global_city_temperature where date_published between '1743-01-01' and '1745-12-01'
        GROUP BY (date_published)) highest
        WHERE g.date_published = highest.date_published
        AND g.average_temperature = highest.highest_temperature
        AND highest.highest_temperature <> 0;"""
        cursor.execute(update_user_cmd)
        record = cursor.fetchall()
        response = jsonify(record)
        response.status_code = 200
        return (response)

    except Exception as e:
        print(e)
        response = jsonify('Failed to get city.')
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()

@app.route('/city', methods=['GET'])
def get_highest_temperature():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='climate',
                                       user='root',
                                       password='root123')
        cursor = conn.cursor()
        year = request.args['year']
        print(year)
        update_user_cmd = """select * from global_city_temperature where year(date_published) >= '%s' order by average_temperature desc limit 1;"""
        bindData = (year)
        cursor.execute(update_user_cmd, bindData)
        record = cursor.fetchall()
        response = jsonify(record)
        response.status_code = 200
        return (response)

    except Exception as e:
        print(e)
        response = jsonify('Failed to get temperature.')
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    app.run(debug=True)


