import json

# Load JSON data
with open('./class-bard.json', 'r') as file:
    data = json.load(file)

# Function to standardize JSON objects
def standardize_json(data):
    # Default keys for class, subclass, classFeature, and subclassFeature objects
    default_class_keys = {
        'name': '', 'source': '', 'page': '', 'srd': False, 'hd': {'number': 0, 'faces': 0}, 
        'proficiency': [], 'spellcastingAbility': '', 'casterProgression': '', 
        'cantripProgression': [], 'spellsKnownProgression': [], 'additionalSpells': [],
        'startingProficiencies': {}, 'startingEquipment': {}, 'multiclassing': {}, 
        'classTableGroups': [], 'classFeatures': [], 'subclassTitle': '', 'fluff': []
    }
    default_subclass_keys = {
        'name': '', 'shortName': '', 'source': '', 'className': '', 'classSource': '', 'page': '', 
        'srd': False, 'additionalSpells': [], 'subclassFeatures': []
    }
    default_class_feature_keys = {
        'name': '', 'source': '', 'page': '', 'className': '', 'classSource': '', 'level': 0, 
        'entries': [], 'isClassFeatureVariant': False
    }
    default_subclass_feature_keys = {
        'name': '', 'source': '', 'page': '', 'className': '', 'classSource': '', 'subclassName': '', 
        'subclassSource': '', 'level': 0, 'entries': [], 'isClassFeatureVariant': False
    }

    def add_missing_keys(obj, default_keys):
        for key, value in default_keys.items():
            if key not in obj:
                obj[key] = value
        return obj

    # Standardize class objects
    data['class'] = [add_missing_keys(cls, default_class_keys) for cls in data['class']]
    
    # Standardize subclass objects
    data['subclass'] = [add_missing_keys(subcls, default_subclass_keys) for subcls in data['subclass']]
    
    # Standardize classFeature objects
    data['classFeature'] = [add_missing_keys(feature, default_class_feature_keys) for feature in data['classFeature']]
    
    # Standardize subclassFeature objects
    data['subclassFeature'] = [add_missing_keys(feature, default_subclass_feature_keys) for feature in data['subclassFeature']]
    
    return data

# Standardize the JSON data
standardized_data = standardize_json(data)

# Save the standardized data back to JSON file
with open('./standardized-class-bard.json', 'w') as file:
    json.dump(standardized_data, file, indent=4)

# Print non-standard parts for review
non_standard_parts = {
    'missing_class_page': [cls for cls in standardized_data['class'] if cls['page'] == ''],
    'missing_subclass_page': [subcls for subcls in standardized_data['subclass'] if subcls['page'] == ''],
    'missing_class_feature_page': [feature for feature in standardized_data['classFeature'] if feature['page'] == ''],
    'missing_subclass_feature_page': [feature for feature in standardized_data['subclassFeature'] if feature['page'] == '']
}

non_standard_parts
