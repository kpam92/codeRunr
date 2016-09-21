drop table if exists user;
create table user (
  id integer primary key autoincrement,
  username text not null,
  email text not null,
  pw_hash text not null
);

drop table if exists snippets;
create table snippets (
  id integer primary key autoincrement,
  title text not null,
  user_id integer not null,
  code text not null,
  pub_date integer
);
