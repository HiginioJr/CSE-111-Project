--User Info
--1
INSERT INTO user (u_username, u_password) VALUES('username', 'password');

--2
UPDATE user SET u_username = 'new_username'
WHERE u_username = 'old_username';

--3
UPDATE user SET u_password = 'new_password'
WHERE u_username = 'username';

--4
DELETE FROM user
WHERE u_username = 'username';

--Park Info
--5
INSERT INTO parks (p_park_code, p_park_name, p_state, p_acres, p_latitude, p_longitude)
VALUES ('park code', 'park name', 'state', 100, 1.00, 1.00);

--6
UPDATE parks SET p_park_name = 'new park name'
WHERE p_park_code = 'park code';

--7
UPDATE parks SET p_latitude = 1.00, p_longitude = 1.00, p_acres = 100
WHERE p_park_code = 'park code';

--Species Info
--8
INSERT INTO species (s_species_id, s_park_name, s_category, s_order, s_family, s_occurrence, s_nativeness, s_abundance, s_seasonality)
VALUES ('species id', 'park name', 'category', 'order', 'family', 'occurence', 'nativeness', 'abundance', 'seasonality');

--9
UPDATE species SET s_abundance = 'new abundance'
WHERE s_species_id = 'species id';

--10
DELETE FROM species
WHERE s_species_id = 'species id';

--Animal Info
--11
INSERT INTO animals (a_species_id, a_scientific_name, a_record_status, a_conservation_ststus)
VALUES ('species id', 'scientific name', 'record status', 'conservation status');

--12
UPDATE animals SET a_record_status = 'record status', a_conservation_ststus = 'conservation status'
WHERE a_species_id = 'species id';

--13
DELETE FROM animals
WHERE a_species_id = 'species id';

--Plant Info
--14
INSERT INTO plants (pl_species_id, pl_scientific_name, pl_record_status, pl_conservation_status)
VALUES ('species id', 'scientific name', 'record status', 'conservation status');

--15
UPDATE plants SET pl_record_status = 'record status', pl_conservation_status = 'conservation status'
WHERE pl_species_id = 'species id';

--16
DELETE FROM plants
WHERE pl_species_id = 'species id';

--Search Saving
--17
INSERT INTO search (se_animal_name, se_park, se_username)
VALUES ('search term', 'park name', 'username');

--18
DELETE FROM search
WHERE se_username = 'username';

--Common Name Info
--19
INSERT INTO common_names (cn_species_id, cn_common_name)
VALUES ('species id', 'common name');

--20
UPDATE common_names SET cn_common_name = 'new name'
WHERE cn_species_id = 'species id';

--21
DELETE FROM common_names
WHERE cn_species_id = 'species id';

--Searching Database

--Search Animals/Plants
--22
SELECT a_scientific_name, cn_common_name, s_park_name, s_category, s_order, s_family
FROM animals, common_names, species
WHERE a_scientific_name = 'Urocyon littoralis'
AND s_species_id = a_species_id
ORDER BY a_scientific_name ASC;

--23
SELECT pl_scientific_name, cn_common_name, s_park_name, s_category, s_order, s_family
FROM plants, common_names, species
WHERE pl_scientific_name = 'Lemna minor'
AND s_species_id = pl_species_id
ORDER BY pl_scientific_name ASC;

--24
SELECT a_scientific_name, s_occurrence, s_nativeness, s_abundance, s_seasonality, a_record_status, a_conservation_ststus
FROM animals, species
WHERE a_scientific_name = 'Urocyon littoralis'
AND s_species_id = a_species_id
ORDER BY a_scientific_name ASC;

--25
SELECT pl_scientific_name, s_occurrence, s_nativeness, s_abundance, s_seasonality, pl_record_status, pl_conservation_status
FROM plants, species
WHERE pl_scientific_name = 'Lemna minor'
AND s_species_id = pl_species_id
ORDER BY pl_scientific_name ASC;

--Search Parks
--26
SELECT p_park_name, p_state, p_acres, p_latitude, p_longitude
FROM parks
WHERE p_park_name = 'Redwood National Park';

--Search Species
--27
SELECT s_species_id, s_category, s_order, s_family, s_occurrence, s_nativeness, s_abundance, s_seasonality
FROM species
WHERE s_species_id = 'CHIS-1002';