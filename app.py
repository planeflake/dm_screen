from flask import Flask, render_template, request, redirect, url_for, jsonify, session, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from neo4j import GraphDatabase
import time
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

db="rpgdb"
username="postgres"
passw="."
hostname="localhost"

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
client = OpenAI(api_key=openai_api_key)

# Neo4j connection
uri = 'neo4j+s://b29956d6.databases.neo4j.io'
user = 'neo4j'
password = '0kc1APDksb8vIkSWOraGix4fulXDzr6d_81Uw5JLDbs'
driver = GraphDatabase.driver(uri, auth=(user, password))

# Dummy player data
players_list = [
    {'username': 'player1'},
    {'username': 'player2'},
    {'username': 'dm'},
    {'username': 'dm2'}
]
db_params = {
    "dbname": "rpgdb",
    "user": "postgres",
    "password": ".",
    "host": "localhost"
}
characters = [
    {"id": 1, "name": "Character 1", "hit_points": 100},
    {"id": 2, "name": "Character 2", "hit_points": 90}
]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_FOLDER = os.path.join(BASE_DIR, 'src/images')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'src/images')
JSON_FILE = os.path.join(BASE_DIR, 'src/images.json')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def startup():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w') as file:
            json.dump({}, file)

def read_json():
    with open(JSON_FILE, 'r') as file:
        return json.load(file)

def write_json(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def generate_detailed_prompt(data):
    chat_input = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Create a detailed description for an image generation prompt based on the following hero details. Do not use the word 'character', use 'hero' instead: {json.dumps(data)}"}
    ]

    try:
        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_input
        )
        detailed_prompt = chat_response.choices[0].message.content
        return detailed_prompt
    except Exception as e:
        print(f"Error generating detailed prompt: {e}")
        return None

def generate_image(prompt):
    print(f"Generating image with prompt: {prompt}")
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def get_characters_for_player(username):
    with driver.session() as session:
        result = session.run(
            "MATCH (p:Player {username: $username})-[:HAS_CHARACTER]->(c:Character) "
            "RETURN c.name AS name, id(c) AS id", username=username)
        characters = [{"name": record["name"], "id": record["id"]} for record in result]
    return characters

def get_spell_slots(class_name, level):
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname=db,
        user=username,
        password=passw,
        host=hostname
    )

    # Create a cursor object
    cur = conn.cursor()

    # Define your query
    query = """
    SELECT slots FROM spell_slots WHERE class_id = (SELECT id from classes where name = %s) and level = %s;
    """
    # Execute the query
    cur.execute(query, (class_name, level))

    # Fetch all the results
    results = cur.fetchall()

    # Assuming there's always at least one result
    if results:
        data = results[0][0]
    else:
        data = None

    #print(data)  # Print the data for debugging

    # Close the cursor and connection
    cur.close()
    conn.close()

    return data

def get_db_connection():
    conn = psycopg2.connect(**db_params)
    return conn

@app.route('/postgrestest')
def postgresindex():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM races")
    races = cur.fetchall()

    cur.execute("SELECT id, name FROM classes")
    classes = cur.fetchall()

    cur.execute("SELECT id, name FROM subclasses")
    subclasses = cur.fetchall()

    cur.execute("SELECT id, name FROM alignments")
    alignments = cur.fetchall()

    cur.execute("SELECT id, name FROM backgrounds")
    backgrounds = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('/postgrestest.html', races=races, classes=classes, subclasses=subclasses, alignments=alignments, backgrounds=backgrounds)

@app.route('/get_starting_equipment', methods=['POST'])
def get_starting_equipment():
    class_id = request.json.get('class')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT default_equipment FROM starting_equipment WHERE class_id = %s", (class_id,))
    equipment = cur.fetchone()
    cur.close()
    conn.close()

    if equipment:
        equipment_options = equipment[0]  # Directly use the fetched data
    else:
        equipment_options = []

    simplified_options = []
    for item_set in equipment_options:
        options = []
        for key, items in item_set.items():
            item_text = ', '.join(
                [f"{item['item']} (x{item['quantity']})" if isinstance(item, dict) else item for item in items]
            )
            options.append({'option': key, 'items': item_text})
        simplified_options.append(options)

    #print('Returning equipment options:', equipment_options)
    print('Returning simplified options:', simplified_options)

    return jsonify(simplified_options)

def get_character_spell_data():
    """select s.slots from spell_slots as s where class_id = 10 and level = 5
    select spell_slot_level,count(*) from spell_slots_usage where character_id = 371
    group by spell_slot_level"""
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT spell_slot_level, count(*) FROM spell_slots_usage WHERE character_id = 371
    GROUP BY spell_slot_level
    """
    cur.execute(query)
    spell_data = cur.fetchall()

    cur.close()
    conn.close()

    return spell_data

def get_conditions():
    with driver.session() as session:
        result = session.run("MATCH (c:Condition) RETURN c.name AS name, c.icon AS icon")
        conditions = [{"name": record["name"], "icon": record["icon"]} for record in result]
    return conditions

def get_characters_for_dm():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (c:Character)-[:BELONGS_TO_CLASS]->(cl:Class),
                  (c)-[:BELONGS_TO_RACE]->(r:Races)
            OPTIONAL MATCH (c)-[:HAS_AC]->(ac:ArmorClass)
            OPTIONAL MATCH (c)-[:HAS_CR]->(cr:ChallengeRating)
            OPTIONAL MATCH (c)-[:HAS_TYPE]->(type:Type)
            RETURN c.name AS characterName, id(c) AS characterId, cl.name AS className, r.name AS raceName,
                   c.level AS level, c.strength AS strength, c.dexterity AS dexterity, 
                   c.constitution AS constitution, c.intelligence AS intelligence,
                   c.wisdom AS wisdom, c.charisma AS charisma, c.token_url AS tokenUrl, 
                   ac.ac AS ac, cr.cr AS cr, type.type AS type, c.hit_points as max_hp, c.hit_points as hp
            """
        )
        characters = []
        spell_data = []
        for record in result:

            spell_data = get_spell_slots(record["className"], record['level'])
            print(spell_data)
            print( record["characterName"])
            print(record["className"])

            characters.append({
                "name": record["characterName"],
                "id": record["characterId"],
                "class": record["className"],
                "race": record["raceName"],
                "level": record["level"],
                "strength": record["strength"],
                "dexterity": record["dexterity"],
                "constitution": record["constitution"],
                "intelligence": record["intelligence"],
                "wisdom": record["wisdom"],
                "charisma": record["charisma"],
                "tokenUrl": record["tokenUrl"],
                "ac": record["ac"],
                "cr": record["cr"],
                "type": record["type"],
                "hp": record['hp'],
                "max_hp": record['hp'],
                "spell_slots" : spell_data,
                "spell_slots_used" :"2,2,2"
            })
        return characters

def cast_a_spell(character_id,spell_id):
    print('Character with ID:' & character_id & 'Casting a spell' & spell_id)
    data = os.open('./src/slots.json')
    slots = json.load(data)
    return slots

def get_character_details(character_id):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (c:Character)-[:BELONGS_TO_CLASS]->(cl:Class),
                  (c)-[:BELONGS_TO_RACE]->(r:Races)
            WHERE id(c) = $character_id
            RETURN c.name AS name, c.level AS level, c.strength AS strength, 
                   c.dexterity AS dexterity, c.constitution AS constitution, 
                   c.intelligence AS intelligence, c.wisdom AS wisdom, 
                   c.charisma AS charisma, c.hit_points AS hit_points, 
                   c.armor_class AS armor_class, c.speed AS speed, 
                   c.alignment AS alignment, c.background AS background, 
                   cl.name AS class, r.name AS race
            """, character_id=character_id)
        return result.single()

def get_classes():
    with driver.session() as session:
        result = session.run("MATCH (c:Class) RETURN c.name AS name")
        classes = [record["name"] for record in result]
    return classes

def get_races():
    with driver.session() as session:
        result = session.run("MATCH (r:Races) RETURN r.name AS name")
        races = [record["name"] for record in result]
    return races

@app.route('/get_speeds', methods=['POST'])
def get_speeds():
    race_id = request.json.get('race')  # Use request.json to get data from JSON payload

    if not race_id:
        return "Race ID is required.", 400

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT type, value FROM speed
    WHERE race_id = %s
    """
    cur.execute(query, (race_id,))
    race_speeds = cur.fetchall()

    cur.close()
    conn.close()

    if race_speeds:
        speeds = "<p><strong>Speeds:</strong></p>"
        for speed in race_speeds:
            speeds += f"""
            <p><strong>{speed[0].replace('_', ' ').title()}:</strong> {speed[1]}</p>
            """
        return speeds
    else:
        return "No speeds found for this race."

@app.route('/get_race_details', methods=['POST'])
def get_race_details():
    race_id = request.json.get('race') 
    print(race_id)
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT 
        r.source, r.id, r.name, r.page, r.size, r.darkvision, r.has_fluff, r.has_fluff_images,
        f.source as fluff_source, f.fluff_data 
    FROM races r
    LEFT JOIN fluff f ON r.id = f.race_id
    WHERE r.id = %s;
    """
    
    cur.execute(query, (race_id,))
    race_details = cur.fetchone()

    query = """
    SELECT type, value FROM speed WHERE race_id = %s
    """
    cur.execute(query, (race_id,))
    race_speeds = cur.fetchall()

    query = """
    SELECT name,source,cover_url FROM source_books WHERE source = %s;"""
    cur.execute(query, (race_details[0],))
    race_source = cur.fetchall()
    print(race_source)

    cur.close()
    conn.close()
    
    source_image_url = race_source[0][2].replace('img','static')
    print(source_image_url)
    if race_details:
        details = f"""
        <div class="container">
        <div class="column">

        <p><strong>Source:</strong> {race_source[0][0]}</p>
        <p><strong>Name:</strong> {race_details[2]}</p>
        <p><strong>Page:</strong> {race_details[3]}</p>
        <p><strong>Size:</strong> {race_details[4]}</p>
        <p><strong>Speeds:</strong></p>
        """
        for speed in race_speeds:
            details += f"<p><strong>{speed[0].replace('_', ' ').title()}:</strong> {speed[1]}</p>"
        
        details += f"""
        <p><strong>Darkvision:</strong> {race_details[5]}</p>
        </div>
        <div class="column">
        <img src= {source_image_url} alt="Cover Image" style="width:200px;height:250px;">
        </div>
        </div>        
        <p><strong>Fluff Data:</strong> {race_details[9]}</p>        
        """
        return details
    else:
        return "No details found for this race."

@app.route('/get_class_details', methods=['POST'])
def get_class_details():
    class_id = request.json.get('class') 
    print('Class ID:' + class_id)
    conn = get_db_connection()
    cur = conn.cursor()

    # First, check if spellcasting_ability is not null
    cur.execute("SELECT spellcasting_ability FROM classes WHERE id = %s", (class_id,))
    spellcasting_ability = cur.fetchone()

    if spellcasting_ability and spellcasting_ability[0] is not None:
        query = """
        SELECT 
            name,
            source,
            page,
            spellcasting_ability,
            caster_progression,
            prepared_spells,
            cantrip_progression,
            spells_known_progression,
            additional_spells
        FROM 
            classes
        WHERE
            id = %s
        """
    else:
        query = """
        SELECT 
            name,
            source,
            page
        FROM 
            classes
        WHERE
            id = %s
        """
    
    cur.execute(query, (class_id,))
    class_details = cur.fetchone()
    cur.close()
    conn.close()
    
    if class_details:
        details = "<p><strong>Class Details:</strong></p>"
        columns = ['name', 'source', 'page', 'spellcasting_ability', 'caster_progression', 'prepared_spells', 'cantrip_progression', 'spells_known_progression', 'additional_spells']
        for i, value in enumerate(class_details):
            if value is not None:
                details += f"<p><strong>{columns[i].replace('_', ' ').title()}:</strong> {value}</p>"
        return details
    else:
        return "No details found for this class."

@app.route('/get_background_details', methods=['POST'])
def get_background_details():
    background_id = request.json.get('background') 
    
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT 
        name, 
        source, 
        description 
    FROM backgrounds 
    WHERE id = %s;
    """
    
    cur.execute(query, (background_id,))
    background_details = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if background_details:
        details = f"""
        <p><strong>Background:</strong> {background_details[0]}</p>
        <p><strong>Source:</strong> {background_details[1]}</p>
        <p><strong>Description:</strong> {background_details[2]}</p>
        """
        return details
    else:
        return "No details found for this background."

@app.route('/get_subclass_details', methods=['POST'])
def get_subclass_details():
    subclass_id = request.form['subclass']
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = """
    SELECT name, source, description FROM subclasses WHERE id = %s;
    """
    
    cur.execute(query, (subclass_id,))
    subclass_details = cur.fetchone()
    
    cur.close()
    conn.close()
    
    details = f"""
    <h3>{subclass_details[0]}</h3>
    <p><strong>Source:</strong> {subclass_details[1]}</p>
    <p><strong>Description:</strong> {subclass_details[2]}</p>
    """
    return details

@app.route('/get_alignment_details', methods=['POST'])
def get_alignment_details():
    alignment_index = int(request.form['alignment'])
    alignments = [
        "Lawful Good", "Neutral Good", "Chaotic Good",
        "Lawful Neutral", "True Neutral", "Chaotic Neutral",
        "Lawful Evil", "Neutral Evil", "Chaotic Evil"
    ]
    alignment = alignments[alignment_index]
    
    details = f"""
   <h3>Alignment: {alignment}</h3>
    """
    return details

@app.route('/get_sources_with_covers', methods=['GET'])
def get_sources_with_covers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, source, cover_image FROM books")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    sources = []
    for row in rows:
        source = {
            'name': row[0],
            'source': row[1],
            'cover_image': row[2]
        }
        sources.append(source)

    return jsonify(sources)

def get_alignments():
    return ['Lawful Good', 'Neutral Good', 'Chaotic Good', 'Lawful Neutral', 'True Neutral', 'Chaotic Neutral', 'Lawful Evil', 'Neutral Evil', 'Chaotic Evil']

def get_backgrounds():
    return ['Acolyte', 'Charlatan', 'Criminal', 'Entertainer', 'Folk Hero', 'Guild Artisan', 'Hermit', 'Noble', 'Outlander', 'Sage', 'Sailor', 'Soldier', 'Urchin']

def get_five_monsters():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (m:Monster)
            OPTIONAL MATCH (m)-[:HAS_AC]->(ac:ArmorClass)
            OPTIONAL MATCH (m)-[:HAS_CR]->(cr:ChallengeRating)
            OPTIONAL MATCH (m)-[:HAS_TYPE]->(type:Type)
            RETURN m.name AS name, ac.ac AS ac, cr.cr AS cr, type.type AS type, m.token_url as tokenUrl
            LIMIT 5
            """
        )
        monsters = []
        for record in result:
            monsters.append({
                "name": record["name"],
                "ac": record["ac"],
                "cr": record["cr"],
                "type": record["type"],
                "tokenUrl": record["tokenUrl"]
            })
        return monsters

def get_all_players():
    with driver.session() as session:
        result = session.run("MATCH (p:Player) RETURN p.username AS username")
        players = [{"username": record["username"]} for record in result]
    return players

def get_all_monsters():
    with driver.session() as session:
        result = session.run("MATCH (m:Monster) RETURN m.name AS name, m.hp_average AS hp, m.dex AS dex, m.con AS con, m.int AS int, m.wis AS wis, m.cha AS cha, m.page AS page")
        monsters = [{"name": record["name"], "hp": record["hp"], "dex": record["dex"], "con": record["con"], "int": record["int"], "wis": record["wis"], "cha": record["cha"], "page": record["page"]} for record in result]
    return monsters

def calculate_skills(character):
    return {
        'Acrobatics': character['dexterity'],
        'Animal Handling': character['wisdom'],
        'Arcana': character['intelligence'],
        'Athletics': character['strength'],
        'Deception': character['charisma'],
        'History': character['intelligence'],
        'Insight': character['wisdom'],
        'Intimidation': character['charisma'],
        'Investigation': character['intelligence'],
        'Medicine': character['wisdom'],
        'Nature': character['intelligence'],
        'Perception': character['wisdom'],
        'Performance': character['charisma'],
        'Persuasion': character['charisma'],
        'Religion': character['intelligence'],
        'Sleight of Hand': character['dexterity'],
        'Stealth': character['dexterity'],
        'Survival': character['wisdom'],
    }

def get_monster_details(monster_name):
    query = """
    MATCH (m:Monster {name: $name})
    OPTIONAL MATCH (m)-[:HAS_SIZE]->(size:Size)
    OPTIONAL MATCH (m)-[:HAS_TYPE]->(type:Type)
    OPTIONAL MATCH (m)-[:HAS_ALIGNMENT]->(alignment:Alignment)
    OPTIONAL MATCH (m)-[:HAS_CR]->(cr:ChallengeRating)
    OPTIONAL MATCH (m)-[:HAS_SPEED]->(speed:Speed)
    OPTIONAL MATCH (m)-[:KNOWS_LANGUAGE]->(language:Language)
    OPTIONAL MATCH (m)-[:HAS_TRAIT]->(trait:Trait)
    OPTIONAL MATCH (m)-[:HAS_ACTION]->(action:Action)
    OPTIONAL MATCH (m)-[:HAS_AC]->(ac:ArmorClass)
    OPTIONAL MATCH (m)-[:HAS_TAG]->(tag:Tag)
    OPTIONAL MATCH (m)-[:HAS_SKILL]->(skill:Skill)
    OPTIONAL MATCH (m)-[:HAS_SAVE]->(save:Save)
    OPTIONAL MATCH (m)-[:CAN_CAST_SPELL_LEVEL_0]->(spell0:Spell)
    OPTIONAL MATCH (m)-[:CAN_CAST_SPELL_LEVEL_1]->(spell1:Spell)
    OPTIONAL MATCH (m)-[:CAN_CAST_SPELL_LEVEL_2]->(spell2:Spell)
    OPTIONAL MATCH (m)-[:CAN_CAST_SPELL_LEVEL_3]->(spell3:Spell)
    OPTIONAL MATCH (m)-[:CAN_CAST_SPELL_LEVEL_4]->(spell4:Spell)
    OPTIONAL MATCH (m)-[:CAN_CAST_SPELL_LEVEL_5]->(spell5:Spell)
    RETURN m, size, type, alignment, cr, speed, language, trait, action, ac, tag, skill, save, 
           collect(distinct spell0) as spell0, collect(distinct spell1) as spell1, 
           collect(distinct spell2) as spell2, collect(distinct spell3) as spell3, 
           collect(distinct spell4) as spell4, collect(distinct spell5) as spell5
    """
    with driver.session() as session:
        start_time = time.time()
        result = session.run(query, name=monster_name)
        end_time = time.time()
        
        monster_details = result.single()
        
        if not monster_details:
            return None
        
        response = {
            "monster": dict(monster_details["m"]),
            "size": dict(monster_details["size"]) if monster_details["size"] else None,
            "type": dict(monster_details["type"]) if monster_details["type"] else None,
            "alignment": dict(monster_details["alignment"]) if monster_details["alignment"] else None,
            "cr": dict(monster_details["cr"]) if monster_details["cr"] else None,
            "speed": dict(monster_details["speed"]) if monster_details["speed"] else None,
            "language": dict(monster_details["language"]) if monster_details["language"] else None,
            "trait": dict(monster_details["trait"]) if monster_details["trait"] else None,
            "action": dict(monster_details["action"]) if monster_details["action"] else None,
            "ac": dict(monster_details["ac"]) if monster_details["ac"] else None,
            "tag": dict(monster_details["tag"]) if monster_details["tag"] else None,
            "skill": dict(monster_details["skill"]) if monster_details["skill"] else None,
            "save": dict(monster_details["save"]) if monster_details["save"] else None,
            "spells": {
                "level_0": [dict(spell) for spell in set(monster_details["spell0"])],
                "level_1": [dict(spell) for spell in set(monster_details["spell1"])],
                "level_2": [dict(spell) for spell in set(monster_details["spell2"])],
                "level_3": [dict(spell) for spell in set(monster_details["spell3"])],
                "level_4": [dict(spell) for spell in set(monster_details["spell4"])],
                "level_5": [dict(spell) for spell in set(monster_details["spell5"])],
            },
            "execution_time": end_time - start_time
        }
        return response

@app.route('/generate_prompt', methods=['POST'])
def generate_prompt():
    data = request.json
    print("Generating prompt with data:", data)
    # Generate detailed prompt
    prompt = generate_detailed_prompt(data)
    if not prompt:
        return jsonify({'error': 'Failed to generate prompt'}), 500

    # Generate image
    image_url = generate_image(prompt)
    if not image_url:
        return jsonify({'error': 'Failed to generate image'}), 500
    
    return jsonify({'images': [image_url]})

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'imageUpload' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['imageUpload']
        image_type = request.form.get('imageType')
        character_id = request.form.get('characterId')

        if not character_id:
            return jsonify({'error': 'No character ID provided'}), 400

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            data = read_json()
            if character_id not in data:
                data[character_id] = {}
            if image_type in data[character_id]:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], data[character_id][image_type]['filename'])
                if os.path.exists(file_path):
                    os.remove(file_path)

            directory = os.path.join(app.config['UPLOAD_FOLDER'], character_id)
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            filename = f"{image_type}.jpg"
            filepath = os.path.join(directory, filename)
            file.save(filepath)
            
            data[character_id][image_type] = {
                'filename': filepath,
                'url': f'/images/{character_id}/{filename}'
            }
            write_json(data)
            
            return jsonify({'success': 'File uploaded successfully', 'url': f'/images/{character_id}/{filename}'}), 200
    except Exception as e:
        app.logger.error(f"Error uploading file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-images', methods=['GET'])
def get_images():
    character_id = request.args.get('characterId')
    data = read_json()
    if character_id in data:
        images = [{'url': data[character_id][key]['url'], 'type': key, 'id': key} for key in data[character_id]]
        return jsonify(images), 200
    return jsonify([]), 200

@app.route('/images/<character_id>/<filename>')
def uploaded_file(character_id, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], character_id), filename)

@app.route('/replace', methods=['POST'])
def replace_file():
    file = request.files['imageUpload']
    replace_image_id = request.form.get('replaceImageId')
    if file:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], replace_image_id))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], replace_image_id))
        return jsonify({'success': 'File replaced successfully', 'url': f'/images/{replace_image_id}'}), 200

@app.route('/remove', methods=['POST'])
def remove_file():
    image_type = request.form.get('imageType')
    character_id = request.form.get('characterId')
    data = read_json()
    if character_id in data and image_type in data[character_id]:
        filepath = data[character_id][image_type]['filename']
        os.remove(filepath)
        del data[character_id][image_type]
        write_json(data)
        return jsonify({'success': 'File removed successfully'}), 200
    return jsonify({'error': 'Image or Character not found'}), 404

@socketio.on('update_health')
def handle_update_health(data):
    character_id = data['character_id']
    new_health = data['new_health']

    with driver.session() as session:
        session.run(
            "MATCH (c:Character) WHERE id(c) = $character_id "
            "SET c.health = $new_health",
            character_id=character_id, new_health=new_health
        )

    emit('health_updated', {'character_id': character_id, 'new_health': new_health}, broadcast=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/players/<username>')
def players_main(username):
    characters = get_characters_for_player(username)
    return render_template('players_main.html', username=username, characters=characters)

@app.route('/load_character/<int:character_id>', methods=['POST'])
def load_character(character_id):
    return redirect(url_for('character_dashboard', character_id=character_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        print(f"Login attempt by username: {username}")  # Debugging print

        if any(player['username'] == username for player in players_list):
            session['username'] = username
            if username == 'dm':
                print(f"Redirecting to DM dashboard for {username}")  # Debugging print
                return redirect(url_for('dm_dashboard', username=username))
            if username == 'dm2':
                print(f"Redirecting to DM2 dashboard for {username}")  # Debugging print
                return redirect(url_for('dm_dashboard2', username=username))
            print(f"Redirecting to player dashboard for {username}")  # Debugging print
            return redirect(url_for('player_dashboard', username=username))
        print("Username not found in players list")  # Debugging print
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/player_dashboard/<username>', methods=['GET', 'POST'])
def player_dashboard(username):
    player_data = next((player for player in players_list if player['username'] == username), None)
    if not player_data:
        return redirect(url_for('home'))

    with driver.session() as session:
        result = session.run(
            """
            MATCH (p:Player {username: $username})-[:HAS_CHARACTER]->(char:Character)-[:BELONGS_TO_CLASS]->(cl:Class)
            RETURN char.name AS name, char.level AS level, cl.name AS class, id(char) as id,
                   char.strength AS strength, char.dexterity AS dexterity,
                   char.constitution AS constitution, char.intelligence AS intelligence,
                   char.wisdom AS wisdom, char.charisma AS charisma
            """,
            username=username
        )
        characters = [{"name": record["name"], "class": record["class"], "level": record["level"],
                       "strength": record["strength"], "dexterity": record["dexterity"], 
                       "constitution": record["constitution"], "intelligence": record["intelligence"], 
                       "wisdom": record["wisdom"], "charisma": record["charisma"],"id": record["id"]} 
                      for record in result]
    
    if request.method == 'POST':
        # Handle form submissions here
        pass

    return render_template('player_dashboard.html', player_data=player_data, characters=characters)

@app.route('/create_character', methods=['GET', 'POST'])
def create_character():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        char_class = request.form['class']
        char_race = request.form['race']
        level = int(request.form['level'])
        strength = int(request.form['strength'])
        dexterity = int(request.form['dexterity'])
        constitution = int(request.form['constitution'])
        intelligence = int(request.form['intelligence'])
        wisdom = int(request.form['wisdom'])
        charisma = int(request.form['charisma'])
        hit_points = int(request.form['hit_points'])
        armor_class = int(request.form['armor_class'])
        speed = int(request.form['speed'])
        alignment = request.form['alignment']
        background = request.form['background']

        with driver.session() as session:
            session.run(
                """
                MERGE (p:Player {username: $username})
                WITH p
                MATCH (cl:Class {name: $char_class})
                WITH p, cl
                MATCH (r:Race {name: $char_race})
                WITH p, cl, r
                CREATE (char:Character {
                    name: $name,
                    level: $level,
                    strength: $strength,
                    dexterity: $dexterity,
                    constitution: $constitution,
                    intelligence: $intelligence,
                    wisdom: $wisdom,
                    charisma: $charisma,
                    hit_points: $hit_points,
                    armor_class: $armor_class,
                    speed: $speed,
                    alignment: $alignment,
                    background: $background
                })
                WITH p, char, cl, r
                CREATE (p)-[:HAS_CHARACTER]->(char)
                WITH p, char, cl, r
                CREATE (char)-[:BELONGS_TO_CLASS]->(cl)
                WITH p, char, cl, r
                CREATE (char)-[:BELONGS_TO_RACE]->(r)
                """,
                username=username, name=name, char_class=char_class, char_race=char_race,
                level=level, strength=strength, dexterity=dexterity, constitution=constitution,
                intelligence=intelligence, wisdom=wisdom, charisma=charisma, hit_points=hit_points,
                armor_class=armor_class, speed=speed, alignment=alignment, background=background
            )

        return redirect(url_for('player_dashboard', username=username))
    else:
        classes = get_classes()
        races = get_races()
        alignments = get_alignments()
        backgrounds = get_backgrounds()
        return render_template('create_character.html', classes=classes, races=races, alignments=alignments, backgrounds=backgrounds)

@app.route('/get_monster/<name>', methods=['GET'])
def get_monster(name):
    monster_details = get_monster_details(name)
    if monster_details:
        return jsonify(monster_details), 200
    else:
        return jsonify({"error": "Monster not found"}), 404

@app.route('/dm_dashboard/<username>', methods=['GET', 'POST'])
def dm_dashboard(username):
    monsters = get_five_monsters()
    characters = get_characters_for_dm()
    conditions=get_conditions()
    return render_template('dm_dashboard.html', monsters=monsters, characters=characters,conditions=conditions)

@app.route('/dm_dashboard2/<username>', methods=['GET', 'POST'])
def dm_dashboard2(username):
    monsters = get_five_monsters()
    characters = get_characters_for_dm()
    conditions=get_conditions()
    return render_template('dm_dashboard2.html', monsters=monsters, characters=characters,conditions=conditions)


@app.route('/character_dashboard/<int:character_id>')
def character_dashboard(character_id):
    character = get_character_details(character_id)
    skills = calculate_skills(character)
    return render_template('character_dashboard.html', character=character, skills=skills,character_id=character_id)

@socketio.on('next_turn')
def handle_next_turn(data):
    socketio.emit('update_turn', data, broadcast=True)

@socketio.on('previous_turn')
def handle_previous_turn(data):
    socketio.emit('update_turn', data, broadcast=True)

@app.route('/api/players')
def get_players():
    with driver.session() as session:
        result = session.run("MATCH (p:Player)-[:HAS_CHARACTER]->(c:Character) RETURN p.username AS username, id(c) AS id, c.name AS name, c.hp AS hp, c.ac AS ac, c.spell AS spell")
        players = [{"username": record["username"], "id": record["id"], "name": record["name"], "hp": record["hp"], "ac": record["ac"], "spell": record["spell"]} for record in result]
    return jsonify(players)

@app.route('/api/monsters')
def get_monsters():
    with driver.session() as session:
        result = session.run("MATCH (m:Monster) RETURN m.name AS name, m.image AS image, m.hp AS hp, m.ac AS ac")
        monsters = [{"name": record["name"], "image": record["image"], "hp": record["hp"], "ac": record["ac"]} for record in result]
    return jsonify(monsters)

@app.template_filter('modifier')
def modifier_filter(score):
    return (score - 10) // 2

app.jinja_env.filters['modifier'] = modifier_filter
@app.route('/images')
def index():
    images = [f for f in os.listdir(IMAGES_FOLDER) if f.endswith('.webp')]
    return render_template('images.html', images=images)

@app.route('/static/<filename>')
def send_image(filename):
    return send_from_directory(IMAGES_FOLDER, filename)

@app.route('/players')
def players():
    players = get_all_players()
    return jsonify(players)

@app.route('/monsters')
def monsters():
    monsters = get_all_monsters()
    return jsonify(monsters)

@app.route('/update_hp', methods=['POST'])
def update_hp():
    data = request.json
    character_id = data.get('character_id')
    new_hp = data.get('hp')

    # Update the character's HP in the database (dummy update for demonstration)
    for char in characters:
        if char['id'] == character_id:
            char['hit_points'] = new_hp
            break

    # Emit the update to all connected clients
    socketio.emit('health_updated', {'character_id': character_id, 'new_health': new_hp})

    return jsonify({'status': 'success', 'new_hp': new_hp})

startup()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
