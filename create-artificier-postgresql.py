import json
import psycopg2

# Load JSON data
try:
    with open('./src/classes/class-artificer.json') as f:
        data = json.load(f)
    print("JSON data loaded successfully:")
    #print(json.dumps(data, indent=4))  # Pretty-print the JSON data
except FileNotFoundError:
    print("File not found. Please check the file path.")
except json.JSONDecodeError:
    print("Error decoding JSON. Please check the JSON file for errors.")
except Exception as e:
    print(f"An error occurred: {e}")


# Connect to PostgreSQL
try:
    conn = psycopg2.connect(dbname="rpgdb", user="postgres", password=".", host="localhost")
    cur = conn.cursor()
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()


# Function to format array literals
def format_array(array):
    return '{' + ','.join(array) + '}'

# Insert data into the class table
for cls in data['class']:
    cur.execute("""
        INSERT INTO class (name, source, page, is_reprinted, hd_number, hd_faces, spellcasting_ability, caster_progression, starting_equipment_additional_from_background)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
    """, (cls['name'], cls['source'], cls['page'], cls['isReprinted'], cls['hd']['number'], cls['hd']['faces'], cls['spellcastingAbility'], cls['casterProgression'], cls['startingEquipment']['additionalFromBackground']))
    class_id = cur.fetchone()[0]
    
    # Insert spells known progression
    for level, spells_known in enumerate(cls['spellsKnownProgression']):
        cur.execute("""
            INSERT INTO spells_known_progression (class_id, level, spells_known)
            VALUES (%s, %s, %s)
        """, (class_id, level + 1, spells_known))
    
    # Insert starting equipment
    equipment_array = format_array(cls['startingEquipment']['default'])
    cur.execute("""
        INSERT INTO starting_equipment (class_id, equipment)
        VALUES (%s, %s)
    """, (class_id, equipment_array))
    
    # Insert class table groups
    for group in cls['classTableGroups']:
        cur.execute("""
            INSERT INTO class_table_groups (class_id, title, col_labels, rows)
            VALUES (%s, %s, %s, %s)
        """, (class_id, group.get('title', ''), format_array(group['colLabels']), json.dumps(group['rows'])))
    
    # Insert fluff
    if 'fluff' in cls:
        for fluff in cls['fluff']:
            cur.execute("""
                INSERT INTO fluff (class_id, name, page, source, type, entries)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (class_id, fluff['name'], fluff.get('page', None), fluff['source'], fluff['type'], json.dumps(fluff['entries'])))
    
    # Insert proficiencies
    for proficiency in cls['proficiency']:
        cur.execute("""
            INSERT INTO proficiency (class_id, proficiency_type, proficiency_value)
            VALUES (%s, %s, %s)
        """, (class_id, 'class', proficiency))
    
    # Insert starting proficiencies
    cur.execute("""
        INSERT INTO starting_proficiencies (class_id, armor, weapons, tools, skills)
        VALUES (%s, %s, %s, %s, %s)
    """, (class_id, format_array(cls['startingProficiencies']['armor']), format_array(cls['startingProficiencies']['weapons']), format_array(cls['startingProficiencies']['tools']), json.dumps(cls['startingProficiencies']['skills'])))
    
    # Insert class features
    for feature in cls['classFeatures']:
        cur.execute("""
            INSERT INTO class_features (class_id, class_feature)
            VALUES (%s, %s)
        """, (class_id, json.dumps(feature)))

# Insert data into the subclass table
for subclass in data['subclass']:
    cur.execute("""
        INSERT INTO subclass (name, short_name, source, class_id, class_source, page, subclass_features)
        VALUES (%s, %s, %s, (SELECT id FROM class WHERE name = %s AND source = %s), %s, %s, %s)
    """, (subclass['name'], subclass['shortName'], subclass['source'], subclass['className'], subclass['classSource'], subclass['classSource'], subclass['page'], json.dumps(subclass['subclassFeatures'])))

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()
