-- Synthetic examples only. Generated from ORM models, not a database dump.

CREATE TABLE items (
	id VARCHAR NOT NULL,
	name VARCHAR,
	description VARCHAR NOT NULL,
	located VARCHAR,
	PRIMARY KEY (id)
);

CREATE INDEX ix_items_id ON items (id);

CREATE INDEX ix_items_name ON items (name);

CREATE TABLE platforms (
	id VARCHAR NOT NULL,
	platform VARCHAR,
	created_at VARCHAR,
	updated_at VARCHAR,
	PRIMARY KEY (id),
	UNIQUE (id)
);

CREATE TABLE stats (
	id VARCHAR NOT NULL,
	platform_id VARCHAR,
	upload_camera INTEGER,
	upload_gallery INTEGER,
	upload_request INTEGER,
	total_upload INTEGER,
	edit_count INTEGER,
	delete_count INTEGER,
	total_images INTEGER,
	org_filesize FLOAT,
	org_latest_filesize FLOAT,
	total_filesize FLOAT,
	calculated_at VARCHAR NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(platform_id) REFERENCES platforms (id)
);

CREATE INDEX ix_stats_id ON stats (id);

CREATE INDEX ix_stats_platform_id ON stats (platform_id);

CREATE TABLE users (
	id VARCHAR NOT NULL,
	platform_id VARCHAR,
	platform_user_id VARCHAR,
	created_at TIMESTAMP WITHOUT TIME ZONE,
	max_storage_mb INTEGER,
	PRIMARY KEY (id),
	UNIQUE (id),
	FOREIGN KEY(platform_id) REFERENCES platforms (id)
);

CREATE INDEX ix_users_platform_id ON users (platform_id);

CREATE TABLE folders (
	id VARCHAR NOT NULL,
	title VARCHAR NOT NULL,
	parent_id VARCHAR,
	user_id VARCHAR,
	created_at VARCHAR,
	updated_at VARCHAR,
	delete_at VARCHAR,
	PRIMARY KEY (id),
	UNIQUE (id),
	FOREIGN KEY(parent_id) REFERENCES folders (id),
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE INDEX ix_folders_delete_at ON folders (delete_at);

CREATE INDEX ix_folders_parent_id ON folders (parent_id);

CREATE INDEX ix_folders_user_id ON folders (user_id);

CREATE TABLE images (
	uuid VARCHAR NOT NULL,
	s3_info VARCHAR,
	s3_filepath VARCHAR,
	filename VARCHAR NOT NULL,
	user_id VARCHAR,
	folder_id VARCHAR,
	lat FLOAT,
	lng FLOAT,
	filesize FLOAT,
	image_resource_type VARCHAR,
	created_at VARCHAR,
	updated_at VARCHAR,
	delete_at VARCHAR,
	address_road VARCHAR,
	address_land VARCHAR,
	address_land_number VARCHAR,
	building_name VARCHAR,
	address_det VARCHAR,
	address_search VARCHAR,
	address_sort VARCHAR,
	is_signed BOOLEAN,
	is_shared BOOLEAN,
	has_det BOOLEAN,
	PRIMARY KEY (uuid),
	UNIQUE (uuid),
	FOREIGN KEY(user_id) REFERENCES users (id),
	FOREIGN KEY(folder_id) REFERENCES folders (id)
);

CREATE INDEX ix_images_address_search ON images (address_search);

CREATE INDEX ix_images_address_sort ON images (address_sort);

CREATE INDEX ix_images_created_at ON images (created_at);

CREATE INDEX ix_images_delete_at ON images (delete_at);

CREATE INDEX ix_images_folder_id ON images (folder_id);

CREATE INDEX ix_images_user_id ON images (user_id);

CREATE TABLE customs (
	id VARCHAR NOT NULL,
	image_id VARCHAR,
	key VARCHAR,
	value VARCHAR,
	created_at VARCHAR,
	updated_at VARCHAR,
	PRIMARY KEY (id),
	UNIQUE (id),
	FOREIGN KEY(image_id) REFERENCES images (uuid)
);

CREATE INDEX ix_customs_image_id ON customs (image_id);

CREATE TABLE filedata (
	uuid VARCHAR NOT NULL,
	org_image_id VARCHAR,
	s3_info VARCHAR,
	s3_filepath VARCHAR,
	filename VARCHAR NOT NULL,
	user_id VARCHAR,
	filesize FLOAT,
	image_resource_type VARCHAR,
	created_at VARCHAR,
	updated_at VARCHAR,
	hashdata VARCHAR,
	resolution VARCHAR,
	PRIMARY KEY (uuid),
	UNIQUE (uuid),
	FOREIGN KEY(org_image_id) REFERENCES images (uuid),
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE INDEX ix_filedata_created_at ON filedata (created_at);

CREATE INDEX ix_filedata_org_image_id ON filedata (org_image_id);

CREATE INDEX ix_filedata_user_id ON filedata (user_id);

CREATE TABLE memos (
	id VARCHAR NOT NULL,
	image_id VARCHAR,
	message VARCHAR,
	is_client BOOLEAN NOT NULL,
	created_at VARCHAR,
	updated_at VARCHAR,
	PRIMARY KEY (id),
	UNIQUE (id),
	FOREIGN KEY(image_id) REFERENCES images (uuid)
);

CREATE INDEX ix_memos_image_id ON memos (image_id);

INSERT INTO platforms (id, platform, created_at, updated_at)
VALUES ('example-platform', 'Example Platform', '2026-01-01', '2026-01-01');
INSERT INTO users (id, platform_id, platform_user_id, created_at, max_storage_mb)
VALUES ('example-user', 'example-platform', 'example-member', '2026-01-01', 10240);
INSERT INTO folders (id, title, parent_id, user_id, created_at, updated_at, delete_at)
VALUES ('example-root', 'Example root', NULL, 'example-user', '2026-01-01', '2026-01-01', NULL),
       ('example-child', 'Example child', 'example-root', 'example-user', '2026-01-01', '2026-01-01', NULL),
       ('example-trash', 'Example deleted folder', 'example-root', 'example-user', '2026-01-01', '2026-01-01', '2026-01-02');
INSERT INTO items (id, name, description, located)
VALUES ('example-item', 'Example item', 'Synthetic practice record', 'Example location');
