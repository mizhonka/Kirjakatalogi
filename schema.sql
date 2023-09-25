CREATE TABLE Books(
    id SERIAL PRIMARY KEY,
    title TEXT,
    author TEXT,
    pub_year INTEGER,
    lang TEXT,
    pagenumber INT
);

CREATE TABLE Genres(
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES Books,
    genre TEXT
);

CREATE TABLE Users(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN
);

CREATE TABLE Read(
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES Books,
    user_id INTEGER REFERENCES Users
);