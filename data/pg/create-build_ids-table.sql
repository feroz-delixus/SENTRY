CREATE TABLE build_ids (
   id  serial PRIMARY KEY,
   build_id serial NOT NULL,
   jobname VARCHAR (100) NOT NULL,
   status VARCHAR ( 7 )  NOT NULL,
   created_on TIMESTAMPTZ DEFAULT Now()
   );