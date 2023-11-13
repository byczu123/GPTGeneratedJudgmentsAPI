CREATE TABLE user (
    user_id INT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE justification (
    justification_id INT PRIMARY KEY,
    user_id INT,
    justification_text TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
