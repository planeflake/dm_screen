import json
from neo4j import GraphDatabase

# Load JSON data
with open('./src/classes/class-artificer.json') as f:
    data = json.load(f)

uri = 'neo4j+s://b29956d6.databases.neo4j.io'
user = 'neo4j'
password = '0kc1APDksb8vIkSWOraGix4fulXDzr6d_81Uw5JLDbs'
driver = GraphDatabase.driver(uri, auth=(user, password))

# Function to execute a query
def execute_query(driver, query):
    with driver.session() as session:
        session.run(query)

# Function to safely get optional properties
def get_property(data, prop):
    return json.dumps(data[prop]) if prop in data else None

# Generate and execute Cypher queries for the Artificer class
def create_artificer_class(driver, data):
    for cls in data['class']:
        class_properties = {
            "hd_number": cls['hd']['number'],
            "hd_faces": cls['hd']['faces'],
            "proficiency": json.dumps(cls['proficiency']),
            "spellcastingAbility": cls['spellcastingAbility'],
            "casterProgression": cls['casterProgression'],
            "page": cls['page'],
            "isReprinted": cls['isReprinted']
        }
        
        optional_properties = {
            "spellsKnownProgression": get_property(cls, 'spellsKnownProgression'),
            "preparedSpells": get_property(cls, 'preparedSpells'),
            "cantripProgression": get_property(cls, 'cantripProgression'),
            "optionalfeatureProgression": get_property(cls, 'optionalfeatureProgression'),
            "subclassTitle": get_property(cls, 'subclassTitle'),
            "fluff": get_property(cls, 'fluff'),
            "otherSources": get_property(cls, 'otherSources')
        }

        class_query = f"""
        MERGE (c:Class {{name: "{cls['name']}", source: "{cls['source']}"}})
        ON CREATE SET 
            c.hd_number = {class_properties['hd_number']}, 
            c.hd_faces = {class_properties['hd_faces']}, 
            c.proficiency = {class_properties['proficiency']}, 
            c.spellcastingAbility = "{class_properties['spellcastingAbility']}",
            c.casterProgression = "{class_properties['casterProgression']}",
            c.page = {class_properties['page']},
            c.isReprinted = {class_properties['isReprinted']}
        """

        for key, value in optional_properties.items():
            if value is not None:
                class_query += f", c.{key} = {value}"

        class_query += " ON MATCH SET "  # Start the ON MATCH SET part
        class_query += f"""
            c.proficiency = {class_properties['proficiency']}, 
            c.spellcastingAbility = "{class_properties['spellcastingAbility']}",
            c.casterProgression = "{class_properties['casterProgression']}",
            c.page = {class_properties['page']},
            c.isReprinted = {class_properties['isReprinted']}
        """

        for key, value in optional_properties.items():
            if value is not None:
                class_query += f", c.{key} = {value}"

        execute_query(driver, class_query)

        # Create Starting Proficiencies
        sp = cls['startingProficiencies']
        sp_query = f"""
        MERGE (sp:StartingProficiencies {{class: "{cls['name']}"}})
        ON CREATE SET 
            sp.armor = {json.dumps(sp['armor'])},
            sp.weapons = {json.dumps(sp['weapons'])},
            sp.tools = {json.dumps(sp['tools'])},
            sp.skills_choice_count = {sp['skills'][0]['choose']['count']}
        """
        execute_query(driver, sp_query)

        for skill in sp['skills'][0]['choose']['from']:
            skill_query = f"""
            MERGE (skill:Skill {{name: "{skill}"}})
            MERGE (sp)-[:CAN_CHOOSE_SKILL_FROM]->(skill)
            """
            execute_query(driver, skill_query)

        # Create Starting Equipment
        se = cls['startingEquipment']
        se_query = f"""
        MERGE (se:StartingEquipment {{class: "{cls['name']}"}})
        ON CREATE SET 
            se.additionalFromBackground = {se['additionalFromBackground']},
            se.default = {json.dumps(se['default'])},
            se.goldAlternative = "{se.get('goldAlternative', 'None')}"
        """
        execute_query(driver, se_query)

        # Create Multiclassing
        mc = cls.get('multiclassing', {})
        if mc:
            mc_query = f"""
            MERGE (mc:Multiclassing {{class: "{cls['name']}"}})
            ON CREATE SET 
                mc.requirements = {json.dumps(mc['requirements'])}
            """
            execute_query(driver, mc_query)

        # Create Class Features
        for feature in cls['classFeatures']:
            feature_query = f"""
            MERGE (f:Feature {{name: "{feature['classFeature'].split('|')[0]}", level: {feature['classFeature'].split('|')[2]}}})
            ON CREATE SET 
                f.description = "{feature['classFeature']}",
                f.gainSubclassFeature = {feature.get('gainSubclassFeature', False)}
            """
            execute_query(driver, feature_query)

            rel_query = f"""
            MATCH (c:Class {{name: "{cls['name']}"}})
            MATCH (f:Feature {{name: "{feature['classFeature'].split('|')[0]}", level: {feature['classFeature'].split('|')[2]}}})
            MERGE (c)-[:HAS_FEATURE]->(f)
            """
            execute_query(driver, rel_query)

        # Create Spell Slots for Artificer
        slot_data = [
            {"level": 1, "slots": [0, 0, 0, 0], "rel_name": "LEVEL_ONE_SPELL_SLOTS"},
            {"level": 2, "slots": [0, 0, 0, 0], "rel_name": "LEVEL_TWO_SPELL_SLOTS"},
            {"level": 3, "slots": [2, 0, 0, 0], "rel_name": "LEVEL_THREE_SPELL_SLOTS"},
            {"level": 4, "slots": [3, 0, 0, 0], "rel_name": "LEVEL_FOUR_SPELL_SLOTS"},
            {"level": 5, "slots": [3, 0, 0, 0], "rel_name": "LEVEL_FIVE_SPELL_SLOTS"},
            {"level": 6, "slots": [3, 0, 0, 0], "rel_name": "LEVEL_SIX_SPELL_SLOTS"},
            {"level": 7, "slots": [4, 2, 0, 0], "rel_name": "LEVEL_SEVEN_SPELL_SLOTS"},
            {"level": 8, "slots": [4, 2, 0, 0], "rel_name": "LEVEL_EIGHT_SPELL_SLOTS"},
            {"level": 9, "slots": [4, 2, 0, 0], "rel_name": "LEVEL_NINE_SPELL_SLOTS"},
            {"level": 10, "slots": [4, 3, 0, 0], "rel_name": "LEVEL_TEN_SPELL_SLOTS"},
            {"level": 11, "slots": [4, 3, 0, 0], "rel_name": "LEVEL_ELEVEN_SPELL_SLOTS"},
            {"level": 12, "slots": [4, 3, 0, 0], "rel_name": "LEVEL_TWELVE_SPELL_SLOTS"},
            {"level": 13, "slots": [4, 3, 2, 0], "rel_name": "LEVEL_THIRTEEN_SPELL_SLOTS"},
            {"level": 14, "slots": [4, 3, 2, 0], "rel_name": "LEVEL_FOURTEEN_SPELL_SLOTS"},
            {"level": 15, "slots": [4, 3, 2, 0], "rel_name": "LEVEL_FIFTEEN_SPELL_SLOTS"},
            {"level": 16, "slots": [4, 3, 3, 0], "rel_name": "LEVEL_SIXTEEN_SPELL_SLOTS"},
            {"level": 17, "slots": [4, 3, 3, 0], "rel_name": "LEVEL_SEVENTEEN_SPELL_SLOTS"},
            {"level": 18, "slots": [4, 3, 3, 0], "rel_name": "LEVEL_EIGHTEEN_SPELL_SLOTS"},
            {"level": 19, "slots": [4, 3, 3, 1], "rel_name": "LEVEL_NINETEEN_SPELL_SLOTS"},
            {"level": 20, "slots": [4, 3, 3, 1], "rel_name": "LEVEL_TWENTY_SPELL_SLOTS"},
        ]

        for slot in slot_data:
            slot_query = f"""
            MERGE (slot:SpellSlot {{subclass: "{cls['name']}", level: {slot['level']}}})
            ON CREATE SET 
                slot.level1_slots = {slot['slots'][0]},
                slot.level2_slots = {slot['slots'][1]},
                slot.level3_slots = {slot['slots'][2]},
                slot.level4_slots = {slot['slots'][3]}
            WITH slot
            MATCH (sc:Subclass {{name: "{cls['name']}"}})
            MERGE (sc)-[:{slot['rel_name']}]->(slot)
            """
            execute_query(driver, slot_query)

# Run the function to create the Artificer class
create_artificer_class(driver, data)

# Close the driver connection
driver.close()
