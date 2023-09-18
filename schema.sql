CREATE TABLE Books(
    id SERIAL PRIMARY KEY,
    title TEXT,
    author TEXT,
    pub_year INTEGER,
    lang TEXT,
    pagenumber INT,
    genre TEXT
)