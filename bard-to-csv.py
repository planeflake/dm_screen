import json
import csv

# Load JSON data
with open('/class-bard.json', 'r') as file:
    data = json.load(file)

# Extract relevant data
classes = data['class']
subclasses = data['subclass']
class_features = data['classFeature']
subclass_features = data['subclassFeature']

# Helper function to write to CSV
def write_csv(filename, fieldnames, rows):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

# Prepare data for CSV files
class_rows = []
subclass_rows = []
class_feature_rows = []
subclass_feature_rows = []

for cls in classes:
    class_rows.append({
        'name': cls['name'],
        'source': cls['source'],
        'page': cls['page'],
        'srd': cls['srd'],
        'hd_number': cls['hd']['number'],
        'hd_faces': cls['hd']['faces'],
        'proficiency': json.dumps(cls['proficiency']),
        'spellcastingAbility': cls.get('spellcastingAbility', ''),
        'casterProgression': cls.get('casterProgression', ''),
        'cantripProgression': json.dumps(cls.get('cantripProgression', [])),
        'spellsKnownProgression': json.dumps(cls.get('spellsKnownProgression', [])),
        'additionalSpells': json.dumps(cls.get('additionalSpells', [])),
        'startingProficiencies': json.dumps(cls.get('startingProficiencies', {})),
        'startingEquipment': json.dumps(cls.get('startingEquipment', {})),
        'multiclassing': json.dumps(cls.get('multiclassing', {})),
        'classTableGroups': json.dumps(cls.get('classTableGroups', [])),
        'classFeatures': json.dumps(cls.get('classFeatures', [])),
        'subclassTitle': cls.get('subclassTitle', ''),
        'fluff': json.dumps(cls.get('fluff', []))
    })

for subclass in subclasses:
    subclass_rows.append({
        'name': subclass['name'],
        'shortName': subclass.get('shortName', ''),
        'source': subclass['source'],
        'className': subclass['className'],
        'classSource': subclass['classSource'],
        'page': subclass['page'],
        'srd': subclass.get('srd', False),
        'additionalSpells': json.dumps(subclass.get('additionalSpells', [])),
        'subclassFeatures': json.dumps(subclass['subclassFeatures'])
    })

for feature in class_features:
    class_feature_rows.append({
        'name': feature['name'],
        'source': feature['source'],
        'page': feature['page'],
        'className': feature['className'],
        'classSource': feature['classSource'],
        'level': feature['level'],
        'entries': json.dumps(feature['entries']),
        'isClassFeatureVariant': feature.get('isClassFeatureVariant', False)
    })

for feature in subclass_features:
    subclass_feature_rows.append({
        'name': feature['name'],
        'source': feature['source'],
        'page': feature['page'],
        'className': feature['className'],
        'classSource': feature['classSource'],
        'subclassName': feature['subclassName'],
        'subclassSource': feature['subclassSource'],
        'level': feature['level'],
        'entries': json.dumps(feature['entries']),
        'isClassFeatureVariant': feature.get('isClassFeatureVariant', False)
    })

# Write data to CSV files
write_csv('classes.csv', class_rows[0].keys(), class_rows)
write_csv('subclasses.csv', subclass_rows[0].keys(), subclass_rows)
write_csv('class_features.csv', class_feature_rows[0].keys(), class_feature_rows)
write_csv('subclass_features.csv', subclass_feature_rows[0].keys(), subclass_feature_rows)
