BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "projects" (
	"id"	VARCHAR NOT NULL,
	"title"	VARCHAR(140),
	"description"	VARCHAR,
	"image"	VARCHAR,
	"mimetype"	VARCHAR,
	"created_by"	INTEGER NOT NULL,
	PRIMARY KEY("id","created_by")
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"email"	VARCHAR(80),
	"username"	VARCHAR(100),
	"password"	VARCHAR,
	"active"	BOOLEAN,
	"is_admin"	BOOLEAN,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "category" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(20),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user_tasks" (
	"user_id"	INTEGER NOT NULL,
	"project_id"	INTEGER NOT NULL,
	PRIMARY KEY("user_id","project_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	FOREIGN KEY("project_id") REFERENCES "projects"("id")
);
CREATE TABLE IF NOT EXISTS "task" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(140),
	"date"	DATE,
	"time"	TIME,
	"project_id"	INTEGER,
	"category"	VARCHAR,
	"checked"	BOOLEAN,
	PRIMARY KEY("id"),
	FOREIGN KEY("category") REFERENCES "category"("id"),
	FOREIGN KEY("project_id") REFERENCES "projects"("id")
);
CREATE TABLE IF NOT EXISTS "user_request" (
	"user_id_mittente"	INTEGER NOT NULL,
	"project_id"	VARCHAR NOT NULL,
	"user_id_destinatario"	INTEGER,
	"accepted"	BOOLEAN,
	"refuse"	BOOLEAN,
	PRIMARY KEY("user_id_mittente","project_id"),
	FOREIGN KEY("project_id") REFERENCES "projects"("id"),
	FOREIGN KEY("user_id_mittente") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "alembic_version" (
	"version_num"	VARCHAR(32) NOT NULL,
	CONSTRAINT "alembic_version_pkc" PRIMARY KEY("version_num")
);
INSERT INTO "projects" VALUES ('70135ff0-cb6f-11ec-931a-a0a4c5806b5e','progetto1','progetto1','contentdiagram.jpg','image/jpeg',3);
INSERT INTO "projects" VALUES ('a0e23b59-cb73-11ec-b7db-a0a4c5806b5e','progetto2','progetto2','contentdiagram.jpg','image/jpeg',2);
INSERT INTO "projects" VALUES ('7c3627ec-cb7a-11ec-97ad-a0a4c5806b5e','sdssd','dsdd','contentdiagram.jpg','image/jpeg',2);
INSERT INTO "projects" VALUES ('66b50708-cb7b-11ec-bcb4-a0a4c5806b5e','asdd','dsdsdsd','contentdiagram.jpg','image/jpeg',3);
INSERT INTO "projects" VALUES ('82e50753-cb7b-11ec-b1ba-a0a4c5806b5e','asas','saaaas','contentdiagram.jpg','image/jpeg',3);
INSERT INTO "projects" VALUES ('44fd65fb-cb7f-11ec-a5ec-a0a4c5806b5e','aSSDSD','ASASSSD','contentdiagram.jpg','image/jpeg',3);
INSERT INTO "projects" VALUES ('568c0097-e521-11ec-8462-fedc79eb40e2','progetto2','ededfdfd','xsd.png','image/png',3);
INSERT INTO "projects" VALUES ('9c32e293-e521-11ec-acf8-fedc79eb40e2','as','sasd','xslt.png','image/png',3);
INSERT INTO "users" VALUES (1,'admin2@libero.it','admin2','admin',1,1);
INSERT INTO "users" VALUES (2,'admin1@libero.it','admin1223233','',1,1);
INSERT INTO "users" VALUES (3,'admin@libero.it','admin','admin',1,1);
INSERT INTO "category" VALUES (1,'High');
INSERT INTO "category" VALUES (2,'Medium');
INSERT INTO "category" VALUES (3,'Low');
INSERT INTO "user_tasks" VALUES (3,'70135ff0-cb6f-11ec-931a-a0a4c5806b5e');
INSERT INTO "user_tasks" VALUES (1,'70135ff0-cb6f-11ec-931a-a0a4c5806b5e');
INSERT INTO "user_tasks" VALUES (2,'70135ff0-cb6f-11ec-931a-a0a4c5806b5e');
INSERT INTO "user_tasks" VALUES (2,'a0e23b59-cb73-11ec-b7db-a0a4c5806b5e');
INSERT INTO "user_tasks" VALUES (2,'7c3627ec-cb7a-11ec-97ad-a0a4c5806b5e');
INSERT INTO "user_tasks" VALUES (3,'66b50708-cb7b-11ec-bcb4-a0a4c5806b5e');
INSERT INTO "user_tasks" VALUES (3,'82e50753-cb7b-11ec-b1ba-a0a4c5806b5e');
INSERT INTO "user_tasks" VALUES (3,'44fd65fb-cb7f-11ec-a5ec-a0a4c5806b5e');
INSERT INTO "user_tasks" VALUES (3,'a0e23b59-cb73-11ec-b7db-a0a4c5806b5e');
INSERT INTO "user_tasks" VALUES (1,'a0e23b59-cb73-11ec-b7db-a0a4c5806b5e');
INSERT INTO "user_tasks" VALUES (3,'568c0097-e521-11ec-8462-fedc79eb40e2');
INSERT INTO "user_tasks" VALUES (2,'568c0097-e521-11ec-8462-fedc79eb40e2');
INSERT INTO "user_tasks" VALUES (1,'568c0097-e521-11ec-8462-fedc79eb40e2');
INSERT INTO "user_tasks" VALUES (3,'9c32e293-e521-11ec-acf8-fedc79eb40e2');
INSERT INTO "user_tasks" VALUES (1,'9c32e293-e521-11ec-acf8-fedc79eb40e2');
INSERT INTO "user_tasks" VALUES (2,'9c32e293-e521-11ec-acf8-fedc79eb40e2');
INSERT INTO "task" VALUES (1,'ciaomondo','2022-05-28','08:19:00.000000','70135ff0-cb6f-11ec-931a-a0a4c5806b5e','Medium',0);
INSERT INTO "task" VALUES (2,'testo','2022-05-22','10:15:00.000000','70135ff0-cb6f-11ec-931a-a0a4c5806b5e','High',0);
INSERT INTO "task" VALUES (3,'bellissimo','2022-05-20','08:20:00.000000','70135ff0-cb6f-11ec-931a-a0a4c5806b5e','Low',0);
INSERT INTO "user_request" VALUES (3,'a0e23b59-cb73-11ec-b7db-a0a4c5806b5e',2,1,0);
INSERT INTO "user_request" VALUES (3,'7c3627ec-cb7a-11ec-97ad-a0a4c5806b5e',2,0,1);
INSERT INTO "user_request" VALUES (1,'a0e23b59-cb73-11ec-b7db-a0a4c5806b5e',2,1,0);
INSERT INTO "user_request" VALUES (1,'66b50708-cb7b-11ec-bcb4-a0a4c5806b5e',3,0,0);
INSERT INTO "user_request" VALUES (1,'44fd65fb-cb7f-11ec-a5ec-a0a4c5806b5e',3,0,0);
INSERT INTO "user_request" VALUES (2,'82e50753-cb7b-11ec-b1ba-a0a4c5806b5e',3,0,0);
INSERT INTO "user_request" VALUES (1,'9c32e293-e521-11ec-acf8-fedc79eb40e2',3,1,0);
COMMIT;
