create database blog1;

use blog1;

create table posts(
	sno int primary key auto_increment,
    title text,
    content text,
    date datetime default current_timestamp
);

drop table posts;
select * from posts;
alter table posts add slug text;

create table contacts(
	sno int primary key auto_increment,
    name text(50),
    email varchar(50),
    phone_num varchar(13),
    message text(500),
    date datetime default current_timestamp
);
drop table contacts;
select * from contacts;

insert into contacts (sno,name,email,phone_num,message) values(1,"tridib","t@gmail.com",123456789,"hello");
insert into contacts (name,email,phone_num,message) values("tridib2","t2@gmail.com",123456780,"hello world");