DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username varchar(30) not null,
  email varchar(50) not null,
  pw_hash varchar(255) not null
);

DROP TABLE IF EXISTS snippets;
CREATE TABLE snippets (
  id SERIAL PRIMARY KEY,
  title varchar(80) not null,
  user_id int not null,
  code varchar(255) not null
);
