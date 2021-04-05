CREATE DATABASE IF NOT EXISTS 'project_employees'  ;
USE 'project_employees';
create table if not exists 'registered_users'('id' int(11) not null auto_increment,
'username' varchar(50) not null , 'password' varchar(255) not null, 'email' varchar(100) not null,
primary key('id'))
engine=InnoDB auto_increment=2 ;