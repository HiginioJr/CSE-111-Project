DROP TABLE IF EXISTS search;
CREATE TABLE search (
    se_search_id INTEGER PRIMARY KEY AUTOINCREMENT,
    se_animal_name string(100) not null,
    se_park string(100)
);