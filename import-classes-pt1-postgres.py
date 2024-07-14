import psycopg2
import json
from psycopg2.extras import Json


def format_pg_array(array):
    return '{' + ','.join('"' + item + '"' for item in array) + '}'

def insert_class_data(cur, class_data):
    cur.execute('''
        INSERT INTO classes (name, source, page, srd, hd_number, hd_faces, spellcasting_ability, caster_progression, prepared_spells)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    ''', (
        class_data['name'],
        class_data['source'],
        class_data['page'],
        class_data.get('srd', False),
        class_data['hd']['number'],
        class_data['hd']['faces'],
        class_data.get('spellcastingAbility'),
        class_data.get('casterProgression'),
        class_data.get('preparedSpells')
    ))
    class_id = cur.fetchone()[0]
    print(f"Inserted class with ID: {class_id}")

    for prof_type in ['armor', 'weapons', 'tools']:
        if prof_type in class_data['startingProficiencies']:
            for proficiency in class_data['startingProficiencies'][prof_type]:
                cur.execute('''
                    INSERT INTO proficiencies (class_id, type, proficiency)
                    VALUES (%s, %s, %s)
                ''', (class_id, prof_type, proficiency))
                print(f"Inserted proficiency for class ID: {class_id}")

    if 'skills' in class_data['startingProficiencies']:
        skills = class_data['startingProficiencies']['skills'][0]['choose']['from']
        count = class_data['startingProficiencies']['skills'][0]['choose']['count']
        cur.execute('''
            INSERT INTO starting_proficiencies (class_id, armor, weapons, tools, skills)
            VALUES (%s, %s, %s, %s, %s)
        ''', (class_id, format_pg_array(class_data['startingProficiencies'].get('armor', [])),
              format_pg_array(class_data['startingProficiencies'].get('weapons', [])),
              format_pg_array(class_data['startingProficiencies'].get('tools', [])),
              Json({'choose': {'from': skills, 'count': count}})))
        print(f"Inserted starting proficiencies for class ID: {class_id}")

    cur.execute('''
        INSERT INTO starting_equipment (class_id, additional_from_background, default_equipment, gold_alternative)
        VALUES (%s, %s, %s, %s)
    ''', (class_id, class_data['startingEquipment'].get('additionalFromBackground'),
          Json(class_data['startingEquipment'].get('default')),
          class_data['startingEquipment'].get('goldAlternative')))
    print(f"Inserted starting equipment for class ID: {class_id}")

    cur.execute('''
        INSERT INTO multiclassing (class_id, requirements, proficiencies_gained)
        VALUES (%s, %s, %s)
    ''', (class_id, Json(class_data['multiclassing']['requirements']),
          Json(class_data['multiclassing']['proficienciesGained'])))
    print(f"Inserted multiclassing for class ID: {class_id}")

    if 'classTableGroups' in class_data:
        spell_slots = class_data['classTableGroups'][0]['rows']
        for level, slots in enumerate(spell_slots, start=1):
            cur.execute('''
                INSERT INTO spell_slots (class_id, level, level1_slots, level2_slots, level3_slots, level4_slots, level5_slots, level6_slots, level7_slots, level8_slots, level9_slots)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (class_id, level, *slots))
            print(f"Inserted spell slots for class ID: {class_id} at level {level}")

    if 'classFeatures' in class_data:
        for feature in class_data['classFeatures']:
            if isinstance(feature, dict):
                feature_name = feature['classFeature']
                description = feature['classFeature']
            else:
                feature_name = feature
                description = feature
            level = int(feature_name.split('||')[-1])
            cur.execute('''
                INSERT INTO class_features (class_id, name, source, page, level, description)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (class_id, feature_name.split('|')[0], class_data['source'], class_data['page'], level, description))
            print(f"Inserted class feature for class ID: {class_id} at level {level}")

    if 'subclass' in class_data:
        for subclass in class_data['subclass']:
            cur.execute('''
                INSERT INTO subclasses (class_id, name, short_name, source, page, spellcasting_ability, caster_progression, additional_spells)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (class_id, subclass['name'], subclass['shortName'], subclass['source'], subclass['page'],
                  subclass.get('spellcastingAbility'), subclass.get('casterProgression'), Json(subclass.get('additionalSpells'))))
            subclass_id = cur.fetchone()[0]
            print(f"Inserted subclass with ID: {subclass_id} for class ID: {class_id}")

            if 'subclassFeatures' in subclass:
                for feature in subclass['subclassFeatures']:
                    if isinstance(feature, dict):
                        feature_name = feature['classFeature']
                        description = feature['classFeature']
                    else:
                        feature_name = feature
                        description = feature
                    level = int(feature_name.split('||')[-1])
                    cur.execute('''
                        INSERT INTO subclass_features (subclass_id, name, level, description)
                        VALUES (%s, %s, %s, %s)
                    ''', (subclass_id, feature_name.split('|')[0], level, description))
                    print(f"Inserted subclass feature for subclass ID: {subclass_id} at level {level}")

def main():
    conn = psycopg2.connect("dbname=rpgdb user=postgres password=. host=localhost")
    cur = conn.cursor()
    
    conn.commit()

    files = [
        './src/classes/class-artificer.json',
        './src/classes/class-druid.json',
        './src/classes/class-paladin.json',
        './src/classes/class-wizard.json',
        './src/classes/class-cleric.json'
    ]

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            for cls in data['class']:
                insert_class_data(cur, cls)
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()