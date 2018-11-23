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

create table food (
  id serial primary key,
  name text,
  en_loc text,
  sv_loc text,
  co2_impresion numeric not null,
  co2_transport_import numeric default null
);
