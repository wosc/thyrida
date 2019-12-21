-- Adapted to sqlite from https://github.com/wosc/pharos-deployment/blob/master/cookbooks/wosc-mailserver/templates/default/schema.sql
CREATE TABLE domains (
  id integer primary key,
  name varchar NOT NULL,
  user_id integer, -- NOT NULL,
  customer varchar default NULL,
  responsible varchar default 'n/a',
  price_plan varchar default 'n/a',
  registry varchar default 'n/a',
  state varchar default 'OK',
  since date default '1970-01-01',
  last_payment date default '1970-01-01',
  payment_until date default '1970-01-01',
  comments text,
  dkim_private_key text,
  is_mx integer NOT NULL default '1'
);

CREATE TABLE mailboxes (
  id integer primary key,
  domain_id integer NOT NULL,
  local_part varchar NOT NULL,
  dotted_address varchar default NULL,
  login varchar NOT NULL,
  password varchar NOT NULL,
  forward varchar default NULL,
  has_mailbox integer NOT NULL default '0',
  has_vacation integer NOT NULL default '0',
  has_spamfilter integer NOT NULL default '0',
  vacation_subject varchar default NULL,
  vacation_body text,
  action varchar NOT NULL,
  mailbox_path varchar NOT NULL,
  uid integer NOT NULL default '105',
  gid integer NOT NULL default '8'
);

CREATE TABLE users (
  id integer primary key,
  login varchar NOT NULL,
  password varchar NOT NULL,
  role varchar NOT NULL default 'mail'
);
