from neo4j import GraphDatabase

# Define the slot data
slot_data = [
    {"level": 1, "slots": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_ONE_SPELL_SLOTS"},
    {"level": 2, "slots": [2, 0, 0, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_TWO_SPELL_SLOTS"},
    {"level": 3, "slots": [3, 0, 0, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_THREE_SPELL_SLOTS"},
    {"level": 4, "slots": [3, 0, 0, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_FOUR_SPELL_SLOTS"},
    {"level": 5, "slots": [4, 2, 0, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_FIVE_SPELL_SLOTS"},
    {"level": 6, "slots": [4, 2, 0, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_SIX_SPELL_SLOTS"},
    {"level": 7, "slots": [4, 3, 0, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_SEVEN_SPELL_SLOTS"},
    {"level": 8, "slots": [4, 3, 0, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_EIGHT_SPELL_SLOTS"},
    {"level": 9, "slots": [4, 3, 2, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_NINE_SPELL_SLOTS"},
    {"level": 10, "slots": [4, 3, 3, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_TEN_SPELL_SLOTS"},
    {"level": 11, "slots": [4, 3, 3, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_ELEVEN_SPELL_SLOTS"},
    {"level": 12, "slots": [4, 3, 3, 0, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_TWELVE_SPELL_SLOTS"},
    {"level": 13, "slots": [4, 3, 3, 1, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_THIRTEEN_SPELL_SLOTS"},
    {"level": 14, "slots": [4, 3, 3, 1, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_FOURTEEN_SPELL_SLOTS"},
    {"level": 15, "slots": [4, 3, 3, 2, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_FIFTEEN_SPELL_SLOTS"},
    {"level": 16, "slots": [4, 3, 3, 2, 0, 0, 0, 0, 0, 0], "rel_name": "LEVEL_SIXTEEN_SPELL_SLOTS"},
    {"level": 17, "slots": [4, 3, 3, 3, 1, 0, 0, 0, 0, 0], "rel_name": "LEVEL_SEVENTEEN_SPELL_SLOTS"},
    {"level": 18, "slots": [4, 3, 3, 3, 1, 0, 0, 0, 0, 0], "rel_name": "LEVEL_EIGHTEEN_SPELL_SLOTS"},
    {"level": 19, "slots": [4, 3, 3, 3, 2, 0, 0, 0, 0, 0], "rel_name": "LEVEL_NINETEEN_SPELL_SLOTS"},
    {"level": 20, "slots": [4, 3, 3, 3, 2, 0, 0, 0, 0, 0], "rel_name": "LEVEL_TWENTY_SPELL_SLOTS"},
]

# Generate Cypher queries
queries = []

for slot in slot_data:
    query = f"""
    MERGE (slot:SpellSlot {{subclass: "Arcane Trickster", level: {slot['level']}}})
    ON CREATE SET 
        slot.level1_slots = {slot['slots'][0]},
        slot.level2_slots = {slot['slots'][1]},
        slot.level3_slots = {slot['slots'][2]},
        slot.level4_slots = {slot['slots'][3]},
        slot.level5_slots = {slot['slots'][4]},
        slot.level6_slots = {slot['slots'][5]},
        slot.level7_slots = {slot['slots'][6]},
        slot.level8_slots = {slot['slots'][7]},
        slot.level9_slots = {slot['slots'][8]},
        slot.level10_slots = {slot['slots'][9]}
    WITH slot
    MATCH (sc:Subclass {{name: "Arcane Trickster"}})
    MERGE (sc)-[:{slot['rel_name']}]->(slot)
    """
    queries.append(query)

uri = 'neo4j+s://b29956d6.databases.neo4j.io'
user = 'neo4j'
password = '0kc1APDksb8vIkSWOraGix4fulXDzr6d_81Uw5JLDbs'
driver = GraphDatabase.driver(uri, auth=(user, password))

# Function to execute a query
def execute_query(driver, query):
    with driver.session() as session:
        session.run(query)

# Execute all the generated queries
for query in queries:
    execute_query(driver, query)

# Close the driver connection
driver.close()
