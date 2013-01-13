-- Table: employees

-- DROP TABLE employees;

CREATE TABLE employees
(
  eid bigint NOT NULL,
  xname character varying,
  email_id character varying,
  CONSTRAINT "PK_employees_eid" PRIMARY KEY (eid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE employees
  OWNER TO eduser;


-- Table: messages

-- DROP TABLE messages;

CREATE TABLE messages
(
  mid bigint NOT NULL,
  subject character varying,
  body character varying,
  sender character varying,
  receiver character varying,
  date timestamp with time zone,
  CONSTRAINT "PK_messages_mid" PRIMARY KEY (mid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE messages
  OWNER TO eduser;


-- Table: messages_aux

-- DROP TABLE messages_aux;

CREATE TABLE messages_aux
(
  mid bigint NOT NULL,
  xfrom character varying,
  xto character varying,
  xfolder character varying,
  xorigin character varying,
  xfile character varying,
  CONSTRAINT "PK_messages_aux" PRIMARY KEY (mid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE messages_aux
  OWNER TO eduser;

  