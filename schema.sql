CREATE TABLE user (
    id CHAR(36) PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password CHAR(60) NOT NULL
);

CREATE TABLE justification (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    user_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
