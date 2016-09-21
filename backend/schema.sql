drop table if exists user;
create table user (
  id integer primary key autoincrement,
  username text not null,
  full_name text,
  email text not null,
  pw_hash text not null
);

drop table if exists snippets;
create table message (
  id integer primary key autoincrement,
  author_id integer not null,
  code text not null,
  pub_date integer
);
