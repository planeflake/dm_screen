import json
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=RPGDB user=postgres password=.")
cur = conn.cursor()

# SQL to create tables
create_tables_sql = """
-- Create table for Class
CREATE TABLE IF NOT EXISTS class (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    source VARCHAR(255),
    page INT,
    is_reprinted BOOLEAN,
    hd_number INT,
    hd_faces INT,
    spellcasting_ability VARCHAR(50),
    caster_progression VARCHAR(50),
    starting_equipment_additional_from_background BOOLEAN
);

-- Create table for Proficiency
CREATE TABLE IF NOT EXISTS proficiency (
    id SERIAL PRIMARY KEY,
    class_id INT REFERENCES class(id),
    proficiency_type VARCHAR(50),
    proficiency_value VARCHAR(50)
);

-- Create table for Starting Proficiencies
CREATE TABLE IF NOT EXISTS starting_proficiencies (
    id SERIAL PRIMARY KEY,
    class_id INT REFERENCES class(id),
    armor TEXT[],
    weapons TEXT[],
    tools TEXT[],
    skills JSONB
);

-- Create table for Class Features
CREATE TABLE IF NOT EXISTS class_features (
    id SERIAL PRIMARY KEY,
    class_id INT REFERENCES class(id),
    class_feature JSONB
);

-- Create table for Spells Known Progression
CREATE TABLE IF NOT EXISTS spells_known_progression (
    id SERIAL PRIMARY KEY,
    class_id INT REFERENCES class(id),
    level INT,
    spells_known INT
);

-- Create table for Starting Equipment
CREATE TABLE IF NOT EXISTS starting_equipment (
    id SERIAL PRIMARY KEY,
    class_id INT REFERENCES class(id),
    equipment TEXT[]
);

-- Create table for Class Table Groups
CREATE TABLE IF NOT EXISTS class_table_groups (
    id SERIAL PRIMARY KEY,
    class_id INT REFERENCES class(id),
    title VARCHAR(255),
    col_labels TEXT[],
    rows JSONB
);

-- Create table for Fluff (Descriptions and Lore)
CREATE TABLE IF NOT EXISTS fluff (
    id SERIAL PRIMARY KEY,
    class_id INT REFERENCES class(id),
    name VARCHAR(255),
    page INT,
    source VARCHAR(255),
    type VARCHAR(255),
    entries JSONB
);

-- Create table for Subclass
CREATE TABLE IF NOT EXISTS subclass (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    short_name VARCHAR(255),
    source VARCHAR(255),
    class_id INT REFERENCES class(id),
    class_source VARCHAR(255),
    page INT,
    subclass_features JSONB
);
"""

# Execute the table creation SQL
cur.execute(create_tables_sql)

conn.commit()
cur.close()
conn.close()
