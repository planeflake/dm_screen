import json
import os

file_path = "./classes.json"
with open(file_path, "r", encoding="utf-8-sig") as file:
    json_data = json.load(file)

def escape_quotes(text):
    return text.replace("'", "''")

def extract_subclasses(json_data):
    subclasses_info = []
    class_id_map = {
        "Artificer": 1,
        "Barbarian": 2,
        "Bard": 3,
        "Cleric": 4,
        "Druid": 5,
        "Fighter": 6,
        "Monk": 7,
        "Paladin": 8,
        "Ranger": 9,
        "Rogue": 10,
        "Sorcerer": 11,
        "Warlock": 12,
        "Wizard": 13,
    }

    for cls in json_data['class']:
        class_name = cls['name']
        class_id = class_id_map.get(class_name, None)
        if not class_id:
            continue
        
        for subclass in cls.get('subclasses', []):
            subclass_name = escape_quotes(subclass['name'])
            subclass_source = escape_quotes(subclass.get('source', 'Unknown'))
            subclass_short_name = escape_quotes(subclass.get('shortName', ''))
            subclass_features = escape_quotes(json.dumps(subclass.get('subclassFeatures', [])))
            
            subclass_info = {
                'class_id': class_id,
                'name': subclass_name,
                'short_name': subclass_short_name,
                'source': subclass_source,
                'subclass_features': subclass_features
            }
            
            subclasses_info.append(subclass_info)
    return subclasses_info

def generate_insert_statements(subclasses_info):
    insert_statements = []
    for idx, subclass in enumerate(subclasses_info, start=21):  # Assuming the next ID starts at 21
        insert_statements.append(f"""
INSERT INTO your_table_name (id, class_id, name, short_name, source, subclass_features)
VALUES ({idx}, {subclass['class_id']}, '{subclass['name']}', '{subclass['short_name']}', '{subclass['source']}', '{subclass['subclass_features']}');
        """)
    return insert_statements

# Extracting subclasses
subclasses_info = extract_subclasses(json_data)

# Generating insert statements
insert_statements = generate_insert_statements(subclasses_info)

# Writing the insert statements to a file
output_file_path = "insert_subclasses.sql"
with open(output_file_path, "w", encoding="utf-8") as file:
    for statement in insert_statements:
        file.write(statement)
        file.write("\n")

print(f"SQL insert statements have been written to {output_file_path}")
