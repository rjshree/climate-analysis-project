# Climate-Analysis-Project

## Steps to setup containers
&emsp;&emsp;&emsp; 1. docker-compose up -d <br/>
&emsp;&emsp;&emsp; 2. Login into mysql container once to avoid mysql errors:<br/> a. docker exec -it climate-db bash followed by b. mysql -u root -proot123

## Tasks
#### 1. Setup a database of your choice. Create a table Global_Land_Temperatures_By_City with an appropriate table schema and load the data of GlobalLandTemperaturesByCity.csv into the table. 

   
   &emsp;&emsp;&emsp; I used MySQL 8.0.29 community server and loaded the data via MySQL Workbench. I faced challenges in loading data in my personal pc due to space issue. Hence I was able to load only 10 lakhs records.

##### &emsp;&emsp;&emsp; Analysis on data:<br />
&emsp;&emsp;&emsp;Total number of records: 8599212<br />
&emsp;&emsp;&emsp;Total number of columns: 7<br />
&emsp;&emsp;&emsp;Null values present in: AverageTemperature, AverageTemperatureUncertainty<br />
&emsp;&emsp;&emsp;Total number of null values in AverageTemperature: 364130<br />
&emsp;&emsp;&emsp;Total number of null values in AverageTemperatureUncertainty: 364130<br />

&emsp;&emsp;&emsp; By considering the above data, designed the table Global_Land_Temperatures_By_City with following Primary Keys:
dt as date_published, city, country, latitude, longitude

#### 2. Use a python web framework, such as Flask or Django, and build a REST web service that accesses the database.
 &emsp;&emsp;&emsp; Implemented using Flask-RESTful framework

#### 2a. Create a new entry in the table.
```bash
curl --location --request POST 'http://127.0.0.1:5000/v1/city' \
--header 'Content-Type: application/json' \
--data-raw '{
    "date":"2022-01-24",
    "avg_temperature":21.21,
    "avg_temperature_uncertainty":24.21,
    "city":"Bangalore",
    "country":"India",
    "latitude":"21.21N",
    "longitude":"24.24S"

}'
```
#### 2b. Update an existing entry by specifying a date and a city name with a provided value of AverageTemperature or AverageTemperatureUncertainty.
```bash
curl --location --request PUT 'http://127.0.0.1:5000/v1/city' \
--header 'Content-Type: application/json' \
--data-raw '{
    "date_published":"2022-01-24",
    "average_temperature":24.24,
    "average_temperature_uncertainty":24.24,
    "city":"Bangalore",
    "country":"India",
    "latitude":"21.21N",
    "longitude":"24.24S"
}'
```
#### 2c. Return the top N cities that have the highest monthly AverageTemperature in a specified time range. Each row is the entry of a city’s highest temperature. All columns should be included in the response.
```bash
curl --location --request GET 'http://127.0.0.1:5000/v1/city?start=1743-01-01&end=1745-12-01'
```

#### 3. Examples
a. Find the entry whose city has the highest AverageTemperature since the
year 2000.
```bash
curl --location --request GET 'http://127.0.0.1:5000/v1/city?year=2000'
```
&emsp;&emsp;&emsp; ![Screenshot](https://github.com/rjshree/climate-analysis-project/blob/master/highesttempsince2000.JPG)

b. Assume the temperature observation of the city last month
breaks the record. It is 0.1 degree higher with the same uncertainty. Create
this entry. <br/>

&emsp;&emsp;&emsp; Here updating the record with highest temperature + 0.1 found from above query(3a) to the previous month of the city resulted from above query.
```bash
curl --location --request POST 'http://127.0.0.1:5000/v1/city' \
--header 'Content-Type: application/json' \
--data-raw '{
    "correction":0.1,
    "year":2000
}'
```
&emsp;&emsp;&emsp; ![Screenshot 3b](https://github.com/rjshree/climate-analysis-project/blob/master/screenshot_3b.JPG)

c. Assume the returned entry has been found erroneous.
The actual average temperature of this entry is 2.5 degrees lower. Update
this entry. <br/>
&emsp;&emsp;&emsp; Decreasing the average temperature resulted from first query by 2.5
```bash
curl --location --request PUT 'http://127.0.0.1:5000/v1/city' \
--header 'Content-Type: application/json' \
--data-raw '{
    "correction":2.5,
    "year":2000
}'
```
&emsp;&emsp;&emsp; ![Screenshot_3c](https://github.com/rjshree/climate-analysis-project/blob/master/screenshot_3c.JPG)

Coding of all the above features took me 6-7 hours. Data loading was consuming a lot of time.
