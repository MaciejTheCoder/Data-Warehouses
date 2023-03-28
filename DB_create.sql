USE DB_source
-- model
CREATE TABLE model (
ID_model int PRIMARY KEY NOT NULL,
name varchar(32),
producer varchar(32)
);

-- driver
CREATE TABLE driver (
ID int PRIMARY KEY NOT NULL,
name_surname varchar(64),
type_of_driver VARCHAR(10)
);

-- tram FACT
CREATE TABLE tram (
ID int PRIMARY KEY NOT NULL,
number_of_repairs int, -- slowly changing dimension
year_of_production int,
model int references model,
side_number VARCHAR(3)
);

-- line
CREATE TABLE line (
line_id int PRIMARY KEY NOT NULL,
line_name varchar(12)
);

-- course FACT
CREATE TABLE course (
course_ID int PRIMARY KEY NOT NULL,
start_date date,
start_time time,
end_time time,
tram int references tram,
line int references line,
driver int references driver,
course_total_time int
);

-- passenger FACT
CREATE TABLE passenger ( 
person_id int PRIMARY KEY NOT NULL,
pesel varchar(11),
name_surname varchar(64)
);

-- stop 
CREATE TABLE tram_stop (
ID int PRIMARY KEY NOT NULL,
city varchar(20),
district varchar(20),
residential varchar(20),
single_stop varchar(32),
name varchar(32),
passenger int references passenger
);

-- stopped_at FACT
CREATE TABLE stopped_at (
ID int PRIMARY KEY NOT NULL,
stop_date date,
stop_time time,
course int references course,
stop int references tram_stop,
num_of_passengers_entering int,
num_of_passengers_leaving int,
number_of_free_seats int
);

-- hangar 
CREATE TABLE hangar (
ID_hang int PRIMARY KEY NOT NULL,
name varchar(128),
num_of_total_plots int
);

-- service_in FACT
CREATE TABLE service_in(
ID_service_in int PRIMARY KEY NOT NULL,
tram int references tram,
hangar int references hangar
);

-- workers_team
CREATE TABLE workers_team (
team_ID int PRIMARY KEY NOT NULL,
num_of_workers int,
manager varchar(128),
hangar int references hangar
);

-- repair FACT
CREATE TABLE repair (
repair_ID int PRIMARY KEY NOT NULL,
start_date date,
end_date date,
complexity int,
tram int references tram,
team int references workers_team
);

DROP TABLE repair
DROP TABLE workers_team
DROP TABLE service_in
DROP TABLE hangar
DROP TABLE stopped_at
DROP TABLE tram_stop
DROP TABLE passenger
DROP TABLE course
DROP TABLE line
DROP TABLE tram
DROP TABLE driver
DROP TABLE model