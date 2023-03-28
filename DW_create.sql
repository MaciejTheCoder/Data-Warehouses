USE KUBAMACIEK

DROP TABLE passenger_FACT
DROP TABLE stopped_at_FACT
DROP TABLE course_FACT
DROP TABLE line
DROP TABLE driver
DROP TABLE tram
DROP TABLE model
DROP TABLE time_table
DROP TABLE date_table
DROP TABLE person
DROP TABLE tram_stop

CREATE TABLE person (
person_id int PRIMARY KEY identity(1, 1),
pesel varchar(11),
name_surname varchar(64)
);

CREATE TABLE tram_stop (
tram_stop_id int PRIMARY KEY identity(1, 1),
single_stop varchar(32),
name varchar(32),
city varchar(20),
district varchar(20),
residential varchar(20)
);

CREATE TABLE date_table (
date_id int PRIMARY KEY identity(1, 1),
date DATE,
year int,
month varchar(10),
day_of_week varchar(10)
);

CREATE TABLE time_table (
time_id int PRIMARY KEY identity(1, 1),
hour int,
minute int,
time_of_day varchar(32)
);

CREATE TABLE model(
model_id int PRIMARY KEY identity(1, 1),
name varchar(32),
producer varchar(32)
);

CREATE TABLE tram (
tram_id int PRIMARY KEY identity(1, 1),
tram_side_number varchar(3),
model_id int FOREIGN KEY REFERENCES model(model_id),
year_of_production int
);

CREATE TABLE driver (
driver_id int PRIMARY KEY identity(1, 1),
name_surname varchar(64),
type_of_driver varchar(10)
);

CREATE TABLE line (
line_id int PRIMARY KEY identity(1, 1),
line_name varchar(12)
);

CREATE TABLE course_FACT (
course_id int PRIMARY KEY identity(1, 1),
date_of_course int FOREIGN KEY REFERENCES date_table(date_id),
start_time int FOREIGN KEY REFERENCES time_table(time_id),
finish_time int FOREIGN KEY REFERENCES time_table(time_id),
tram_id int FOREIGN KEY REFERENCES tram(tram_id),
driver_id int FOREIGN KEY REFERENCES driver(driver_id),
line_id int FOREIGN KEY REFERENCES line(line_id),
course_total_time int
);

CREATE TABLE stopped_at_FACT (
course_id int FOREIGN KEY REFERENCES course_FACT(course_id),
tram_stop_id int FOREIGN KEY REFERENCES tram_stop(tram_stop_id),
stop_time_id int FOREIGN KEY REFERENCES time_table(time_id),
number_of_passengers_entering int,
number_of_passenger_leaving int,
number_of_free_seats int
)

CREATE TABLE passenger_FACT (
person_id int FOREIGN KEY REFERENCES person(person_id),
start_stop_id int FOREIGN KEY REFERENCES tram_stop(tram_stop_id),
leave_stop_id int FOREIGN KEY REFERENCES tram_stop(tram_stop_id)
);