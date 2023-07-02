CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS locations(
	id uuid DEFAULT uuid_generate_v4 (),
	name VARCHAR,
	latitude double precision,
	longitude double precision,
	PRIMARY KEY (id)
);
