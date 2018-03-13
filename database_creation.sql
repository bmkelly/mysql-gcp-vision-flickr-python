CREATE DATABASE project_muy;
USE project_muy;

CREATE TABLE Photographer(
  ID smallint unsigned not null auto_increment,
  Username varchar(40),
  PRIMARY KEY(ID),
  CONSTRAINT UC_Photographer UNIQUE (Username)
);

CREATE TABLE Photo(
  ID smallint unsigned not null auto_increment,
  Path varchar(200),
  Name varchar(100),
  PhotographerID smallint unsigned,
  FOREIGN KEY(PhotographerID) REFERENCES Photographer(ID),
  PRIMARY KEY(ID),
  CONSTRAINT UC_Photo UNIQUE (Name)
);

CREATE TABLE Label ( 
  ID smallint unsigned not null auto_increment,
  Score float unsigned, 
  Topicality float unsigned,
  Mid varchar(20),
  Description varchar(40),
  ImageID smallint unsigned,
  PRIMARY KEY (ID),
  FOREIGN KEY (ImageID) REFERENCES Photo(ID),
  CONSTRAINT UC_Label UNIQUE (Score, Topicality, Description, Mid, ImageID)
);



show tables;
DESCRIBE Photographer;
DESCRIBE Photo;
DESCRIBE Label;

