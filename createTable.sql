create table users
(
  id   serial not null
    constraint users_pk
      primary key,
  data jsonb
    constraint users_data_proper_email
      check ((data ->> 'email'::text) ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'::text)
);

alter table users
  owner to cptwarcybkjxed;

create unique index users_data_uindex
  on users ((data ->> 'email'::text));

ALTER TABLE users ADD CONSTRAINT email_must_exist CHECK (data ?    'email');