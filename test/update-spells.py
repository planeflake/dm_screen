import pandas as pd

# Define the character data
character_data = [
    {"name": "Aasimar", "classname": "Bard", "level": 4, "spellslotlevel": 4, "slots": "[4, 3, 0, 0, 0, 0, 0, 0, 0]", "cantrips_known": None, "spells_known": None},
    {"name": "Aarakocra", "classname": "Wizard", "level": 3, "spellslotlevel": 3, "slots": "[4, 2, 0, 0, 0, 0, 0, 0, 0]", "cantrips_known": None, "spells_known": None},
    {"name": "Aven", "classname": "Fighter", "level": 5, "spellslotlevel": None, "slots": None, "cantrips_known": None, "spells_known": None},
    {"name": "Aetherborn", "classname": "Druid", "level": 2, "spellslotlevel": None, "slots": None, "cantrips_known": None, "spells_known": None},
    {"name": "Aarakocra", "classname": "Rogue", "level": 5, "spellslotlevel": None, "slots": None, "cantrips_known": None, "spells_known": None},
    {"name": "Aasimar", "classname": "Cleric", "level": 2, "spellslotlevel": None, "slots": None, "cantrips_known": None, "spells_known": None}
]

# Define the spell information data
spell_info_data = [
    # Bard spell and cantrip information
    {"class": "Bard", "subclass": "", "level": 1, "spellsknown": 4, "cantripsknown": 2},
    {"class": "Bard", "subclass": "", "level": 2, "spellsknown": 5, "cantripsknown": 2},
    {"class": "Bard", "subclass": "", "level": 3, "spellsknown": 6, "cantripsknown": 2},
    {"class": "Bard", "subclass": "", "level": 4, "spellsknown": 7, "cantripsknown": 3},
    {"class": "Bard", "subclass": "", "level": 5, "spellsknown": 8, "cantripsknown": 3},
    {"class": "Bard", "subclass": "", "level": 6, "spellsknown": 9, "cantripsknown": 3},
    {"class": "Bard", "subclass": "", "level": 7, "spellsknown": 10, "cantripsknown": 3},
    {"class": "Bard", "subclass": "", "level": 8, "spellsknown": 11, "cantripsknown": 3},
    {"class": "Bard", "subclass": "", "level": 9, "spellsknown": 12, "cantripsknown": 3},
    {"class": "Bard", "subclass": "", "level": 10, "spellsknown": 14, "cantripsknown": 4},
    {"class": "Bard", "subclass": "", "level": 11, "spellsknown": 15, "cantripsknown": 4},
    {"class": "Bard", "subclass": "", "level": 12, "spellsknown": 15, "cantripsknown": 4},
    {"class": "Bard", "subclass": "", "level": 13, "spellsknown": 16, "cantripsknown": 4},
    {"class": "Bard", "subclass": "", "level": 14, "spellsknown": 18, "cantripsknown": 4},
    {"class": "Bard", "subclass": "", "level": 15, "spellsknown": 19, "cantripsknown": 4},
    {"class": "Bard", "subclass": "", "level": 16, "spellsknown": 19, "cantripsknown": 4},
    {"class": "Bard", "subclass": "", "level": 17, "spellsknown": 20, "cantripsknown": 4},
    {"class": "Bard", "subclass": "", "level": 18, "spellsknown": 22, "cantripsknown": 4},
    {"class": "Bard", "subclass": "", "level": 19, "spellsknown": 22, "cantripsknown": 4},
    {"class": "Bard", "subclass": "", "level": 20, "spellsknown": 22, "cantripsknown": 4},
    # Wizard spell and cantrip information
    {"class": "Wizard", "subclass": "", "level": 1, "spellsknown": 6, "cantripsknown": 3},
    {"class": "Wizard", "subclass": "", "level": 2, "spellsknown": 8, "cantripsknown": 3},
    {"class": "Wizard", "subclass": "", "level": 3, "spellsknown": 10, "cantripsknown": 3},
    {"class": "Wizard", "subclass": "", "level": 4, "spellsknown": 12, "cantripsknown": 4},
    {"class": "Wizard", "subclass": "", "level": 5, "spellsknown": 14, "cantripsknown": 4},
    {"class": "Wizard", "subclass": "", "level": 6, "spellsknown": 16, "cantripsknown": 4},
    {"class": "Wizard", "subclass": "", "level": 7, "spellsknown": 18, "cantripsknown": 4},
    {"class": "Wizard", "subclass": "", "level": 8, "spellsknown": 20, "cantripsknown": 4},
    {"class": "Wizard", "subclass": "", "level": 9, "spellsknown": 22, "cantripsknown": 4},
    {"class": "Wizard", "subclass": "", "level": 10, "spellsknown": 24, "cantripsknown": 5},
    {"class": "Wizard", "subclass": "", "level": 11, "spellsknown": 26, "cantripsknown": 5},
    {"class": "Wizard", "subclass": "", "level": 12, "spellsknown": 28, "cantripsknown": 5},
    {"class": "Wizard", "subclass": "", "level": 13, "spellsknown": 30, "cantripsknown": 5},
    {"class": "Wizard", "subclass": "", "level": 14, "spellsknown": 32, "cantripsknown": 5},
    {"class": "Wizard", "subclass": "", "level": 15, "spellsknown": 34, "cantripsknown": 5},
    {"class": "Wizard", "subclass": "", "level": 16, "spellsknown": 36, "cantripsknown": 5},
    {"class": "Wizard", "subclass": "", "level": 17, "spellsknown": 38, "cantripsknown": 5},
    {"class": "Wizard", "subclass": "", "level": 18, "spellsknown": 40, "cantripsknown": 5},
    {"class": "Wizard", "subclass": "", "level": 19, "spellsknown": 42, "cantripsknown": 5},
    {"class": "Wizard", "subclass": "", "level": 20, "spellsknown": 44, "cantripsknown": 5}
]

# Convert the data to DataFrames
df_characters = pd.DataFrame(character_data)
df_spells = pd.DataFrame(spell_info_data)

# Initialize columns for spellsknown and cantripsknown arrays
df_characters['cantrips_known'] = df_characters['classname'].apply(lambda x: [None] * 20)
df_characters['spells_known'] = df_characters['classname'].apply(lambda x: [None] * 20)

# Fill in the cantrips_known and spells_known arrays
for index, row in df_characters.iterrows():
    classname = row['classname']
    for level in range(1, 21):
        spell_info = df_spells[(df_spells['class'] == classname) & (df_spells['level'] == level)]
        if not spell_info.empty:
            df_characters.at[index, 'cantrips_known'][level - 1] = spell_info.iloc[0]['cantripsknown']
            df_characters.at[index, 'spells_known'][level - 1] = spell_info.iloc[0]['spellsknown']

print(df_characters)