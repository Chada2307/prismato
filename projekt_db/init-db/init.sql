CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    username varchar(50) UNIQUE NOT NULL,
    passwd_hash varchar(255) NOT NULL,
    created_at timestamp DEFAULT now()
);

CREATE TABLE photos ( 
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_path varchar(255) NOT NULL,
    thumbnail_path varchar(255),
    file_size integer,
    captured_at timestamp,
    camera_model varchar(100),
    latitude numeric(9,6),
    longitude numeric(9,6),
    exif_raw jsonb
);

CREATE TABLE people ( 
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name varchar(100) NOT NULL
);

CREATE TABLE faces ( 
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    photo_id uuid NOT NULL REFERENCES photos(id) ON DELETE CASCADE,
    person_id uuid REFERENCES people(id) ON DELETE SET NULL,
    bounding_box jsonb,
    embedding vector(128)
);

CREATE INDEX idx_photos_captured_at ON photos (captured_at DESC);
CREATE INDEX idx_photos_owner ON photos (owner_id);
CREATE INDEX idx_faces_photos ON faces (photo_id);
CREATE INDEX idx_faces_embedding ON faces USING hnsw (embedding vector_cosine_ops);
