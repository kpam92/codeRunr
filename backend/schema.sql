drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null,
  full_name text,
  image_url text,
);

drop table if exists snippets;
create table snippets (
  id integer primary key autoincrement,
  title text not null,
  body text not null
);
