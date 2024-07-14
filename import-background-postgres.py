import json
import psycopg2
from psycopg2.extras import Json

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="rpgdb",
    user="postgres",
    password="."
)
cur = conn.cursor()
conn.commit()

# Load JSON data
with open('./src/data/fluff-backgrounds.json') as f:
    data = json.load(f)

# Insert data into tables
for idx, background in enumerate(data['backgroundFluff']):
    print(f"Inserting background {idx+1} of {len(data['backgroundFluff'])}: {background['name']}")
    cur.execute('''
        INSERT INTO backgrounds (name, source, description)
        VALUES (%s, %s, %s)
        RETURNING id
    ''', (background['name'], background['source'], json.dumps(background['entries'])))
    background_id = cur.fetchone()[0]

    if 'images' in background:
        for image in background['images']:
            cur.execute('''
                INSERT INTO background_images (background_id, image_path)
                VALUES (%s, %s)
            ''', (background_id, image['href']['path']))

    if 'entries' in background:
        for entry in background['entries']:
            if isinstance(entry, dict):
                trait_name = entry.get('name', 'Unnamed Trait')
                trait_description = json.dumps(entry.get('entries', []))
                cur.execute('''
                    INSERT INTO background_traits (background_id, name, description)
                    VALUES (%s, %s, %s)
                ''', (background_id, trait_name, trait_description))

# Commit changes
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()