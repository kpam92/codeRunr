drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
<<<<<<< HEAD
  password text not null,
  full_name text,
  image_url text,
=======
  password_digest text not null,
  full_name text,
  image_url text,
  session_token text not null
>>>>>>> 9f5fa5ce9a72c574479fd02ffd04d5bb9277d787
);

drop table if exists snippets;
create table snippets (
  id integer primary key autoincrement,
  title text not null,
  body text not null
);
