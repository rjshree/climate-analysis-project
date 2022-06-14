import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Float, String, DateTime, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from constants import *
from sqlalchemy.sql.expression import func, extract
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(os.path.basename(__file__))
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)
Base = declarative_base()


class Instance(Base):
    __tablename__ = 'Global_Land_Temperatures_By_City'

    date_published = Column('date_published', DateTime, primary_key= True)
    average_temperature = Column('average_temperature',Float)
    average_temperature_uncertainty = Column('average_temperature_uncertainty', Float)
    city = Column('city',String(100), primary_key= True)
    country = Column('country',String(100), primary_key= True)
    latitude = Column('latitude', String(100), primary_key= True)
    longitude = Column('longitude', String(100), primary_key= True)

    def __repr__(self):
        return '{"date":"%s", "avg_temperature":"%s",  "average_temperature_uncertainty":"%s","city":"%s","country":"%s","latitude":"%s", "longitude":"%s"}' \
               %(self.date_published, self.average_temperature, self.average_temperature_uncertainty, self.city, self.country, self.latitude, self.longitude)

def get_mysql_engine(host, port, database, user, password):
    config = {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password
    }
    connection_string = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(config.get('user'), config.get('password'),
                                                                     config.get('host'), config.get('port'),
                                                                     config.get('database'))
    engine = db.create_engine(connection_string)
    return engine

def get_mysql_session():
    engine = get_mysql_engine(MYSQL_HOST,MYSQL_PORT,MYSQL_DATABASE,MYSQL_USER,MYSQL_PASSWORD)
    Session = sessionmaker(bind=engine)
    # Base.metadata.create_all(engine)
    return Session()


def get_item_by_monthly(start_date, end_date):
    """ Below is the query that gets executed
                SELECT g.* FROM global_city_temperature g,
                (SELECT date_published, MAX(average_temperature) AS highest_temperature
                FROM global_city_temperature where date_published between '1743-01-01' and '1745-12-01'
                GROUP BY (date_published)) highest
                WHERE g.date_published = highest.date_published
                AND g.average_temperature = highest.highest_temperature
                AND highest.highest_temperature <> 0;"""
    try:
        mysql_session = get_mysql_session()
        sub_query = mysql_session.query(Instance.date_published,
                    func.max(Instance.average_temperature).label('highest_temperature')).filter(
                    Instance.date_published.between(start_date, end_date)).group_by(Instance.date_published).subquery()
        result = mysql_session.query(Instance).filter(Instance.date_published == sub_query.c.date_published,
                                                           Instance.average_temperature == sub_query.c.highest_temperature,
                                                           sub_query.c.highest_temperature != 0).all()
        return result
    except Exception as e:
        mysql_session.rollback()
        logger.info(f"Error in fetching {e}")
        return {'status': 'Error in fetching records'}
    finally:
        mysql_session.close()


def get_item_by_year(year):

    try:
        mysql_session = get_mysql_session()
        result = mysql_session.query(Instance).filter(extract('year', Instance.date_published) >= year).order_by(
            Instance.average_temperature.desc()).first()
        return result
    except Exception as e:
        mysql_session.rollback()
        return {'status': 'Error in fetching records'}
    finally:
        mysql_session.close()


def create_item(args):

    insert = Instance(date_published=datetime.strptime(args.date_published, '%Y-%m-%d').date(),
                      average_temperature=float(args.average_temperature),
                      average_temperature_uncertainty=float(args.average_temperature_uncertainty), city=args.city,
                      country=args.country, latitude=args.latitude, longitude=args.longitude)

    try:
        insert_session = get_mysql_session()
        insert_session.add(insert)
        insert_session.commit()
    except Exception as e:
        insert_session.rollback()
    finally:
        insert_session.close()

def update_item_by_city_and_date(args):
    try:

        update_session = get_mysql_session()
        update_session.query(Instance).filter(Instance.city == args.city,
                                              Instance.date_published == args.date_published).update(
            {'average_temperature': args.average_temperature,
             'average_temperature_uncertainty': args.average_temperature_uncertainty})
        update_session.commit()
    except Exception as e:
        update_session.rollback()
    finally:
        update_session.close()

def update_item_by_year(args):
    try:
        update_session = get_mysql_session()
        update_session.execute(
            "update city_temperature as dest, (select * from city_temperature where year(date_published)>=2000 order by average_temperature desc limit 1) as src set dest.average_temperature=dest.average_temperature - :val where dest.date_published=src.date_published and dest.city=src.city;", {'val': args.correction})
        update_session.commit()
    except Exception as e:
        update_session.rollback()
    finally:
        update_session.close()

def create_item_by_condition(year, correction):
    """
    INSERT INTO `climate`.`global_city_temperature`
(`date_published`,
`average_temperature`,
`average_temperature_uncertainty`,
`city`,
`country`,
`latitude`,
`longitude`)
(select
g.date_published,
g.average_temperature+0.1,
g.average_temperature_uncertainty,
g.city,
g.country,
g.latitude,
g.longitude from global_city_temperature g, (select date_published, city from global_city_temperature  where year(date_published) >= 2000 order by average_temperature desc limit 1) as src  where g.date_published = DATE_SUB(src.date_published, INTERVAL 1 MONTH) and g.city=src.city) ;
    :return:
    """
    instance = get_item_by_year(year)
    print("queried instance", instance)
    last_month = instance.date_published - relativedelta(months=1)
    instance.average_temperature +=0.1
    instance.date_published = last_month
    print(" updated instance", instance)
    try:
        session = get_mysql_session()
        record = session.query(Instance).filter(Instance.date_published == instance.date_published, Instance.city == instance.city).first()
        print(record)
        if record:
            session.query(Instance).filter(Instance.city == instance.city,
                                              Instance.date_published == instance.date_published).update(
            {Instance.average_temperature: instance.average_temperature})
        else:
            session.add(instance)

        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return instance


class CustomResponse:
    def __init__(self, message="Internal server error", status=500):
        self.body={
            "status": status,
            "message": message
        }