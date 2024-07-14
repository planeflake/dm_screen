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

# Load JSON data
with open('./src/data/fluff-races.json', 'r') as f:
    data = json.load(f)

fluff_data = data['raceFluff']

# Count total races
total_races = len(fluff_data)
print(f"Total races: {total_races}")

# Iterate over each race's fluff data
for idx, fluff in enumerate(fluff_data):
    print(f"Inserting race {idx+1} of {total_races}: {fluff['name']}")

    # Get the race ID
    cur.execute("SELECT id FROM races WHERE name = %s AND source = %s", (fluff['name'], fluff['source']))
    race_id = cur.fetchone()

    if race_id:
        race_id = race_id[0]

        # Ensure fluff data is a dictionary
        if isinstance(fluff, dict):
            # Insert fluff data, serializing any dictionaries
            fluff_query = """
                INSERT INTO fluff (race_id, name, source, fluff_data)
                VALUES (%s, %s, %s, %s)
            """
            fluff_values = (race_id, fluff['name'], fluff['source'], json.dumps(fluff.get('entries', {})))
            print(cur.mogrify(fluff_query, fluff_values).decode('utf-8'))
            cur.execute(fluff_query, fluff_values)

            # Insert fluff images if they exist and are a list
            if 'images' in fluff and isinstance(fluff['images'], list):
                for image in fluff['images']:
                    if isinstance(image, dict) and 'href' in image and isinstance(image['href'], dict):
                        image_query = """
                            INSERT INTO fluff_images (race_id, image_path, title)
                            VALUES (%s, %s, %s)
                        """
                        image_values = (race_id, image['href'].get('path'), image.get('title'))
                        print(cur.mogrify(image_query, image_values).decode('utf-8'))
                        cur.execute(image_query, image_values)
        else:
            print(f"Skipping fluff data for {fluff['name']} because it's not a dictionary.")
    else:
        print(f"Race {fluff['name']} not found in the races table.")

# Commit the transaction
conn.commit()

# Close the connection
cur.close()
conn.close()