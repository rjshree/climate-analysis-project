# import mysql.connector
# from mysql.connector import Error
#
#
# def connect_db():
#     try:
#         connection = mysql.connector.connect(host='localhost',
#                                              database='climate',
#                                              user='root',
#                                              password='root123')
#
#         if connection.is_connected():
#             cursor = connection.cursor()
#             # return connection
#             db_Info = connection.get_server_info()
#             print("Connected to MySQL Server version ", db_Info)
#
#             cursor.execute("select * from climate.city_temp where city='Rajashree';")
#             record = cursor.fetchone()
#             print("You're connected to database: ", record)
#
#     except Error as e:
#         print("Error while connecting to MySQL", e)
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#             print("MySQL connection is closed")
#
# if __name__ == '__main__':
#     connect_db()
#     # app.run(debug=True)
import dateutil
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
given_date = datetime.strptime('2013-07-01', '%Y-%m-%d').date()
last_day_of_prev_month = given_date-relativedelta(months=1)
# start_day_of_prev_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)

# For printing results
# print("First day of prev month:", start_day_of_prev_month)
print("Last day of prev month:", last_day_of_prev_month)