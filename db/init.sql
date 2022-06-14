CREATE DATABASE climate;
use climate;

CREATE TABLE `Global_Land_Temperatures_By_City` (
  `date_published` date NOT NULL,
  `average_temperature` float DEFAULT NULL,
  `average_temperature_uncertainty` float DEFAULT NULL,
  `city` varchar(75) NOT NULL,
  `country` varchar(75) NOT NULL,
  `latitude` varchar(10) NOT NULL,
  `longitude` varchar(10) NOT NULL,
  PRIMARY KEY (`date_published`,`city`,`country`,`latitude`,`longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `climate`.`Global_Land_Temperatures_By_City`
(`date_published`,
`average_temperature`,
`average_temperature_uncertainty`,
`city`,
`country`,
`latitude`,
`longitude`) values
('2022-06-14',35.6,0.54,'Chennai','India','13.0827N', '80.2707E'),
('2022-05-14',39.6,0.44,'Chennai','India','13.0827N', '80.2707E');