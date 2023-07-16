CREATE DATABASE IF NOT EXISTS lab3;
use lab3;

DROP TABLE IF EXISTS TakeCourse;
DROP TABLE IF EXISTS TakeProj;
DROP TABLE IF EXISTS Publication;
DROP TABLE IF EXISTS Project;
DROP TABLE IF EXISTS Class;
DROP TABLE IF EXISTS Teacher;
DROP TABLE IF EXISTS Paper;

create table Paper(
	PaperID integer primary key,
    papername char(255),
    publisher char(255),
    pubyear date,
    type integer,
    level integer,
	check (type in (1, 2, 3, 4)),
    check (level in (1, 2, 3, 4, 5, 6))
);

create table Teacher(
	ID char(5) primary key,
    teachername char(255),
    sexual integer,
    title integer,
    check (sexual in (1, 2)),
    check (title in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))
);

create table Class(
	Classnum char(255) primary key,
    classname char(255),
    classhour integer,
    quality integer,
    check (quality in (1,2))
);

create table Project(
	Projectnum char(255) primary key,
    projname char(255),
    projsource char(255),
    projtype integer,
    budget float,
    beginyear integer,
    endyear integer,
    check (projtype in (1, 2, 3, 4, 5))
);

create table Publication(
	TeacherID char(5),
	PaperID integer,
    pubrank integer,
    iscoauthor Boolean,
	primary key (TeacherID , PaperID),
    foreign key (TeacherID) references Teacher (ID) on delete cascade,
    foreign key (PaperID) references Paper (PaperID) on delete cascade,
	check (pubrank >= 1)
);

create table TakeProj(
	TeacherID char(5),
	Projectnum char(255),
    projrank integer,
    cost float,
	primary key (TeacherID , Projectnum),
    foreign key (TeacherID) references Teacher (ID) on delete cascade,
    foreign key (Projectnum) references Project (Projectnum) on delete cascade,
	check (projrank >= 1)
);

create table TakeCourse(
	TeacherID char(5),
    Classnum char(255),
    teachyear integer,
    semester integer,
    takehours integer,
    primary key (TeacherID , Classnum),
    foreign key (TeacherID) references Teacher (ID) on delete cascade,
    foreign key (Classnum) references Class (Classnum) on delete cascade,
    check (semester in (1, 2, 3))
);