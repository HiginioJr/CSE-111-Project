DROP TABLE IF EXISTS park_species;
CREATE TABLE park_species(
    ps_park_code string(4) NOT NULL,
    ps_species_id string(100) NOT NULL
);