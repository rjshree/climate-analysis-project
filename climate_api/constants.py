import os


# os.environ['HOST'] = 'localhost'
# os.environ['PORT'] = '3306'
# os.environ['DBNAME'] = 'climate'
# os.environ['DB_USER'] = 'root'
# os.environ['DB_PASSWORD'] = 'root123'
# os.environ['LOG_LEVEL'] = 'ERROR'

MYSQL_HOST= os.environ['HOST']
MYSQL_PORT= os.environ['PORT']
MYSQL_DATABASE= os.environ['DBNAME']
MYSQL_USER= os.environ['DB_USER']
MYSQL_PASSWORD= os.environ['DB_PASSWORD']
LOG_LEVEL = os.environ['LOG_LEVEL']