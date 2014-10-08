# run the following commands with root user
# create schema
CREATE DATABASE itjuzi DEFAULT CHARACTER SET utf8;
CREATE TABLE itjuzi.invest_event (
  id INT NOT NULL AUTO_INCREMENT UNIQUE,
  event_time VARCHAR(1024) NOT NULL,
  invester VARCHAR(1024) NOT NULL,
  company_name VARCHAR(1024) NOT NULL,
  raised_money VARCHAR(1024) NOT NULL,
  round VARCHAR(1024) NOT NULL,
  scope VARCHAR(1024) NOT NULL,
  scraped_time TIMESTAMP NOT NULL);

# grant the perviledge to user spider
GRANT ALL PRIVILEGES ON itjuzi.* TO 'spider'@'localhost' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON itjuzi.* TO 'spider'@'%' WITH GRANT OPTION;

GRANT ALL PRIVILEGES ON itjuzi.* TO 'spider'@'localhost' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON itjuzi.* TO 'spider'@'%' WITH GRANT OPTION;

