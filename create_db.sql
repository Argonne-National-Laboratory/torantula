CREATE TABLE pages_visited (
  domain varchar(30) not null,
  URL varchar(256) not null,
  date_accessed datetime not null,
  PRIMARY KEY (URL(100), date_accessed)
);
