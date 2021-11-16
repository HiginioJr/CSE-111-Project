DROP TABLE IF EXISTS parks;
CREATE TABLE parks (
    p_park_code string(4) not null,
    p_park_name string(100) not null,
    p_state string(2) not null,
    p_acres int not null,
    p_latitude real not null,
    p_longitude real not null
);

DROP TABLE IF EXISTS species;
CREATE TABLE species (
    s_species_id string(100) not null,
    s_park_name string(100) not null,
    s_category string(100) not null,
    s_order string(100),
    s_family string(100),
    s_occurrence string(100),
    s_nativeness string(100),
    s_abundance string(100),
    s_seasonality string(100)
);

DROP TABLE IF EXISTS animals;
CREATE TABLE animals (
    a_species_id string(100) not null,
    a_scientific_name string(100) not null,
    a_record_status string(100) not null,
    a_conservation_ststus string(100)
);

DROP TABLE IF EXISTS plants;
CREATE TABLE plants (
    pl_species_id string(100) not null,
    pl_scientific_name string(100) not null,
    pl_record_status string(100) not null,
    pl_conservation_status string(100)
);

DROP TABLE IF EXISTS common_names;
CREATE TABLE common_names (
    cn_species_id string(100) not null,
    cn_common_name string(100) not null
);

DROP TABLE IF EXISTS search;
CREATE TABLE search (
    se_animal_name string(100) not null,
    se_park string(100)
);

DROP TABLE IF EXISTS user;
CREATE TABLE user (
    u_username string(100) not null,
    u_password string(100) not null
);