DROP TABLE IF EXISTS user_searches;
CREATE TABLE user_searches(
    us_username string(100) REFERENCES user(u_username) ON DELETE SET NULL ON UPDATE CASCADE,
    us_search_id INT REFERENCES search(se_search_id) ON DELETE SET NULL ON UPDATE CASCADE
);