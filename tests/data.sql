CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:260000$aohyx9TYWwET7dvb$b4e41a446d9cfd3a249c978c8b28c3f1b3ffa979da3bad2a98750f0cbcaf7b56')

