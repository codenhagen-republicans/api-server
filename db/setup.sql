create user green_api with login password 'green_api';

create database green_api
    encoding 'UTF8'
    owner green_api;
grant all on database green_api to green_api;

\connect green_api green_api;

create table test (
    id              bigserial    primary key,
    other_thing     text
);
