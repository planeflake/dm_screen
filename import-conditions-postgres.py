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

# Load JSON data
with open('./src/data/conditionsdiseases.json', 'r') as f:
    data_conditions = json.load(f)

with open('./src/data/fluff-conditionsdiseases.json', 'r') as f:
    data_fluff = json.load(f)

# Insert conditions
conditions_data = data_conditions['condition']
for idx, condition in enumerate(conditions_data):
    print(f"Inserting condition {idx + 1} of {len(conditions_data)}: {condition['name']}")
    condition_query = """
        INSERT INTO conditions (name, source, page, srd, entries, has_fluff_images)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    condition_values = (
        condition['name'],
        condition['source'],
        condition.get('page', None),
        condition.get('srd', False),
        Json(condition.get('entries', [])),
        condition.get('hasFluffImages', False)
    )
    cur.execute(condition_query, condition_values)
    condition_id = cur.fetchone()[0]

    # Insert fluff data for conditions
    for fluff in data_fluff['conditionFluff']:
        if fluff['name'] == condition['name']:
            fluff_query = """
                INSERT INTO condition_fluff (condition_id, name, source, images)
                VALUES (%s, %s, %s, %s)
            """
            fluff_values = (
                condition_id,
                fluff['name'],
                fluff['source'],
                Json(fluff.get('images', []))
            )
            print(cur.mogrify(fluff_query, fluff_values).decode('utf-8'))
            cur.execute(fluff_query, fluff_values)

# Insert diseases
diseases_data = data_conditions['disease']
for idx, disease in enumerate(diseases_data):
    print(f"Inserting disease {idx + 1} of {len(diseases_data)}: {disease['name']}")
    disease_query = """
        INSERT INTO diseases (name, source, page, entries)
        VALUES (%s, %s, %s, %s)
    """
    disease_values = (
        disease['name'],
        disease['source'],
        disease.get('page', None),
        Json(disease.get('entries', []))
    )
    cur.execute(disease_query, disease_values)

# Insert status
status_data = data_conditions['status']
for idx, status in enumerate(status_data):
    print(f"Inserting status {idx + 1} of {len(status_data)}: {status['name']}")
    status_query = """
        INSERT INTO status (name, source, page, srd, entries)
        VALUES (%s, %s, %s, %s, %s)
    """
    status_values = (
        status['name'],
        status['source'],
        status.get('page', None),
        status.get('srd', False),
        Json(status.get('entries', []))
    )
    cur.execute(status_query, status_values)

# Commit the transaction
conn.commit()

# Close the connection
cur.close()
conn.close()