DROP TABLE IF EXISTS "user";

CREATE TABLE "user" (
  id SERIAL,
  email varchar(200) DEFAULT NULL,
  username varchar(45) DEFAULT NULL,
  first_name varchar(45) DEFAULT NULL,
  last_name varchar(45) DEFAULT NULL,
  hashed_password varchar(200) DEFAULT NULL,
  is_active boolean DEFAULT NULL,
  role varchar(45) DEFAULT NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS todo;

CREATE TABLE todo (
  id SERIAL,
  title varchar(200) DEFAULT NULL,
  description varchar(200) DEFAULT NULL,
  priority integer  DEFAULT NULL,
  complete boolean  DEFAULT NULL,
  "owner" integer  DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY ("owner") REFERENCES "user"(id)
);