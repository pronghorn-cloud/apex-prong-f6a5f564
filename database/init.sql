-- Initial database schema for Power Policy

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
CREATE TABLE IF NOT EXISTS policies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    document_type_id INTEGER REFERENCES document_types(id),
    current_version_id INTEGER REFERENCES policy_versions(id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'Draft' NOT NULL,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    search_vector TSVECTOR
);

-- Add a GIN index for faster full-text search
CREATE INDEX IF NOT EXISTS policies_search_idx ON policies USING GIN (search_vector);

-- Create a function to update the search_vector
CREATE OR REPLACE FUNCTION update_policy_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector = to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.description, ''));
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

-- Create a trigger to update search_vector on insert or update
DROP TRIGGER IF EXISTS trg_update_policy_search_vector ON policies;
CREATE TRIGGER trg_update_policy_search_vector
BEFORE INSERT OR UPDATE OF title, description ON policies
FOR EACH ROW EXECUTE FUNCTION update_policy_search_vector();


CREATE TABLE IF NOT EXISTS user_roles (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
INSERT INTO users (username, password_hash, email) VALUES
('admin', '$2b$12$5h/d/M.E.T.h.e.r.e.a.l.H.a.s.h.f.o.r.a.d.m.i.n.p.a.s.s.w.d', 'admin@example.com') -- Hashed 'adminpass'

-- Add some default roles
INSERT INTO roles (name) VALUES ('Admin'), ('Editor'), ('Reviewer'), ('Viewer') ON CONFLICT (name) DO NOTHING;

-- Add a default admin user (password 'adminpass')
INSERT INTO users (username, password_hash, email) VALUES
('admin', '$2b$12$K.F.L.M.N.O.P.Q.R.S.T.U.V.W.X.Y.Z.1.2.3.4.5.6.7.8.9.0', 'admin@example.com') -- This is a placeholder, use a proper hash in production
ON CONFLICT (username) DO NOTHING;

-- Assign admin role to the default admin user
INSERT INTO user_roles (user_id, role_id) VALUES
((SELECT id FROM users WHERE username = 'admin'), (SELECT id FROM roles WHERE name = 'Admin'))
ON CONFLICT (user_id, role_id) DO NOTHING;
