create user green_api with login password 'green_api';

GRANT pg_read_server_files TO green_api;

drop database if exists green_api;

create database green_api
    encoding 'UTF8'
    owner green_api;
grant all on database green_api to green_api;

\connect green_api green_api;

create table test (
    id              bigserial    primary key,
    other_thing     text
);

drop table if exists food;

create table food_raw (
  name text,
  co2_impresion text not null,
  co2_transport_import text default null
);

COPY food_raw from '/docker-entrypoint-initdb.d/dummy_co2.csv'
  DELIMITER ',' CSV HEADER QUOTE '"';

create table food (
  id serial primary key,
  name text,
  co2_impresion numeric not null,
  co2_transport_import numeric default null
);

insert into food (
  name,
  co2_impresion,
  co2_transport_import
)
select
  name,
  cast(co2_impresion as float),
  case
    when co2_transport_import = 'null'
      then null
    else cast(co2_transport_import as float) end
from food_raw;
