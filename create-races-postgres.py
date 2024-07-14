import json
import psycopg2

# Load the JSON data
with open('./src/data/races.json', 'r') as f:
    data = json.load(f)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="rpgdb",
    user="postgres",
    password="."
)
cur = conn.cursor()

# Get the total number of races
total_races = len(data['race'])

# Insert data into the races table
for idx, race in enumerate(data['race'], start=1):
    print(f"Processing race {idx} of {total_races}: {race.get('name')}")

    speed_walk = None
    speed_fly = None
    speed_swim = None
    speed_climb = None
    speed_burrow = None

    # Check if speed is a dictionary or an integer
    if isinstance(race.get('speed'), dict):
        speed_walk = race['speed'].get('walk')
        speed_fly = race['speed'].get('fly')
        speed_swim = race['speed'].get('swim')
        speed_climb = race['speed'].get('climb')
        speed_burrow = race['speed'].get('burrow')
    elif isinstance(race.get('speed'), int):
        speed_walk = race['speed']

    race_query = """
        INSERT INTO races (
            name, source, page, is_reprinted, size, speed_walk, speed_fly, speed_swim, speed_climb, speed_burrow, 
            darkvision, sound_clip_path, has_fluff, has_fluff_images
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
    """
    race_values = (
        race.get('name'),
        race.get('source'),
        race.get('page'),
        race.get('isReprinted', False),
        race.get('size')[0] if race.get('size') else None,
        speed_walk,
        speed_fly,
        speed_swim,
        speed_climb,
        speed_burrow,
        race.get('darkvision'),
        race.get('soundClip', {}).get('path') if race.get('soundClip') else None,
        race.get('hasFluff', False),
        race.get('hasFluffImages', False)
    )
    print(cur.mogrify(race_query, race_values).decode('utf-8'))
    cur.execute(race_query, race_values)
    race_id = cur.fetchone()[0]

    # Insert data into the abilities table
    if race.get('ability'):
        for ability in race['ability']:
            if isinstance(ability, dict):  # Ensure ability is a dictionary
                for ability_name, value in ability.items():
                    if isinstance(value, (int, float)):  # Ensure value is a number
                        ability_query = """
                            INSERT INTO abilities (race_id, ability, value) VALUES (%s, %s, %s)
                        """
                        ability_values = (race_id, ability_name, value)
                        print(cur.mogrify(ability_query, ability_values).decode('utf-8'))
                        cur.execute(ability_query, ability_values)
                    else:
                        print(f"Skipping ability with non-numeric value: {ability_name}: {value}")

    # Insert data into the speed table
    if isinstance(race.get('speed'), dict):
        for speed_type, value in race['speed'].items():
            speed_query = """
                INSERT INTO speed (race_id, type, value) VALUES (%s, %s, %s)
            """
            speed_values = (race_id, speed_type, value)
            print(cur.mogrify(speed_query, speed_values).decode('utf-8'))
            cur.execute(speed_query, speed_values)

    # Insert data into the proficiencies table
    if race.get('languageProficiencies'):
        for proficiency in race['languageProficiencies']:
            for prof_type, has_prof in proficiency.items():
                if has_prof:
                    proficiency_query = """
                        INSERT INTO proficiencies (race_id, type, proficiency) VALUES (%s, 'language', %s)
                    """
                    proficiency_values = (race_id, prof_type)
                    print(cur.mogrify(proficiency_query, proficiency_values).decode('utf-8'))
                    cur.execute(proficiency_query, proficiency_values)

    if race.get('weaponProficiencies'):
        for proficiency in race['weaponProficiencies']:
            for prof_type, has_prof in proficiency.items():
                if has_prof:
                    proficiency_query = """
                        INSERT INTO proficiencies (race_id, type, proficiency) VALUES (%s, 'weapon', %s)
                    """
                    proficiency_values = (race_id, prof_type)
                    print(cur.mogrify(proficiency_query, proficiency_values).decode('utf-8'))
                    cur.execute(proficiency_query, proficiency_values)

    if race.get('armorProficiencies'):
        for proficiency in race['armorProficiencies']:
            for prof_type, has_prof in proficiency.items():
                if has_prof:
                    proficiency_query = """
                        INSERT INTO proficiencies (race_id, type, proficiency) VALUES (%s, 'armor', %s)
                    """
                    proficiency_values = (race_id, prof_type)
                    print(cur.mogrify(proficiency_query, proficiency_values).decode('utf-8'))
                    cur.execute(proficiency_query, proficiency_values)

    if race.get('toolProficiencies'):
        for proficiency in race['toolProficiencies']:
            for prof_type, has_prof in proficiency.items():
                if has_prof:
                    proficiency_query = """
                        INSERT INTO proficiencies (race_id, type, proficiency) VALUES (%s, 'tool', %s)
                    """
                    proficiency_values = (race_id, prof_type)
                    print(cur.mogrify(proficiency_query, proficiency_values).decode('utf-8'))
                    cur.execute(proficiency_query, proficiency_values)

    # Insert data into the traits table
    if race.get('entries'):
        for entry in race['entries']:
            if isinstance(entry, dict):  # Ensure entry is a dictionary
                traits_query = """
                    INSERT INTO traits (race_id, name, description) VALUES (%s, %s, %s)
                """
                traits_values = (race_id, entry.get('name'), json.dumps(entry.get('entries')))
                print(cur.mogrify(traits_query, traits_values).decode('utf-8'))
                cur.execute(traits_query, traits_values)
            elif isinstance(entry, str):  # Handle entry as a string
                traits_query = """
                    INSERT INTO traits (race_id, name, description) VALUES (%s, %s, %s)
                """
                traits_values = (race_id, entry, None)
                print(cur.mogrify(traits_query, traits_values).decode('utf-8'))
                cur.execute(traits_query, traits_values)

    # Insert data into the subraces table
    if race.get('subraces'):
        for subrace in race['subraces']:
            subraces_query = """
                INSERT INTO subraces (race_id, name, ability_modifiers, traits) VALUES (%s, %s, %s, %s)
            """
            subraces_values = (race_id, subrace.get('name'), json.dumps(subrace.get('ability')), json.dumps(subrace.get('entries')))
            print(cur.mogrify(subraces_query, subraces_values).decode('utf-8'))
            cur.execute(subraces_query, subraces_values)

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()