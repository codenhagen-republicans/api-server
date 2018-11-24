create user green_api with login password 'green_api';

GRANT pg_read_server_files TO green_api;

drop database if exists green_api;

create database green_api
    encoding 'UTF8'
    owner green_api;
grant all on database green_api to green_api;

\connect green_api green_api;
 
create table food (
  id serial primary key,
  name text,
  co2_impresion numeric not null,
  co2_transport_import numeric default null
);

INSERT INTO food (id,name,co2_impresion,co2_transport_import)
  VALUES
  (DEFAULT,'tomat',0.8,null),
  (DEFAULT,'lök',0.4,null),
  (DEFAULT,'grön paprika',0.7,null),
  (DEFAULT,'salt',0,null),
  (DEFAULT,'tomatpuré',0.8,null),
  (DEFAULT,'nötkött',13.9,null),
  (DEFAULT,'svinkött',4.6,null),
  (DEFAULT,'kycklingkött',5.5,null),
  (DEFAULT,'fårkött',21.4,null),
  (DEFAULT,'gurka',0.8,null),
  (DEFAULT,'potatis',0.2,null),
  (DEFAULT,'vit choklad',2.7,null),
  (DEFAULT,'mörk choklad',0.9,null),
  (DEFAULT,'sokeri',1.0,null),
  (DEFAULT,'frukt fiber',0.9,null),
  (DEFAULT,'äggvita',2.0,null);

create table footprint (
  id serial primary key,
  ean text,
  co2 numeric not null
);

INSERT INTO footprint (id,ean,co2)
  VALUES
  (DEFAULT,'6410405175724',0.54),
  (DEFAULT,'6410405175687',0.18);