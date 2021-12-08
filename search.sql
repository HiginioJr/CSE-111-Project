DROP TABLE IF EXISTS search;
CREATE TABLE search (
    se_search_id INTEGER PRIMARY KEY AUTOINCREMENT,
    se_bio_name string(100) not null,
    se_park string(100),
    se_search_type string(10)
);