import json
import psycopg2

# Load the Bard class JSON file
with open('./src/classes/class-bard.json', 'r') as f:
    data = json.load(f)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="rpgdb",
    user="postgres",
    password=".",
    host="localhost"
)
cur = conn.cursor()

# Function to execute queries
def execute_query(query, values):
    cur.execute(query, values)

# Parse and insert class data
bard_class = data['class'][0]
class_query = '''
    INSERT INTO classes (name, source, page, srd, hd_number, hd_faces, proficiency, spellcasting_ability, caster_progression, cantrip_progression, spells_known_progression, additional_spells)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
'''
class_values = (
    bard_class['name'],
    bard_class['source'],
    bard_class['page'],
    bard_class['srd'],
    bard_class['hd']['number'],
    bard_class['hd']['faces'],
    json.dumps(bard_class['proficiency']),
    bard_class['spellcastingAbility'],
    bard_class['casterProgression'],
    json.dumps(bard_class['cantripProgression']),
    json.dumps(bard_class['spellsKnownProgression']),
    json.dumps(bard_class.get('additionalSpells', []))
)
cur.execute(class_query, class_values)
class_id = cur.fetchone()[0]

# Insert class features
for feature in bard_class['classFeatures']:
    if isinstance(feature, dict):
        name = feature['classFeature']
        gain_subclass_feature = feature.get('gainSubclassFeature', False)
    else:
        name = feature
        gain_subclass_feature = False
    feature_query = '''
        INSERT INTO class_features (class_id, name, source, page, level, entries, is_class_feature_variant)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    '''
    feature_values = (
        class_id,
        name.split('|')[0],
        bard_class['source'],
        bard_class['page'],
        int(name.split('|')[-1]),
        json.dumps(feature),
        'UA' in name
    )
    cur.execute(feature_query, feature_values)

# Insert subclass data
for subclass in data['subclass']:
    subclass_query = '''
        INSERT INTO subclasses (class_id, name, source, page, additional_spells)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    '''
    subclass_values = (
        class_id,
        subclass['name'],
        subclass['source'],
        subclass['page'],
        json.dumps(subclass.get('additionalSpells', []))
    )
    cur.execute(subclass_query, subclass_values)
    subclass_id = cur.fetchone()[0]

    # Insert subclass features
    for feature in subclass['subclassFeatures']:
        feature_query = '''
            INSERT INTO subclass_features (subclass_id, name, source, page, level, entries, is_subclass_feature_variant)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (subclass_id, name, level) DO UPDATE
            RETURNING id;
        '''
        feature_values = (
            subclass_id,
            feature.split('|')[0],
            subclass['source'],
            subclass['page'],
            int(feature.split('|')[-1]),
            json.dumps(feature),
            'UA' in feature
        )
        cur.execute(feature_query, feature_values)

# Commit the transaction and close the connection
conn.commit()
cur.close()
conn.close()
