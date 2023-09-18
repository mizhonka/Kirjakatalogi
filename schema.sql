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