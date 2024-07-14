import pandas as pd

# Define the character data
character_data = [
    {"name": "Aasimar", "classname": "Bard", "level": 4, "spellslotlevel": 4, "slots": "[4, 3, 0, 0, 0, 0, 0, 0, 0]", "cantrips_known": None, "spells_known": None},
    {"name": "Aarakocra", "classname": "Wizard", "level": 3, "spellslotlevel": 3, "slots": "[4, 2, 0, 0, 0, 0, 0, 0, 0]", "cantrips_known": None, "spells_known": None},
    {"name": "Aven", "classname": "Fighter", "level": 5, "spellslotlevel": None, "slots": None, "cantrips_known": None, "spells_known": None},
    {"name": "Aetherborn", "classname": "Druid", "level": 2, "spellslotlevel": None, "slots": None, "cantrips_known": None, "spells_known": None},
    {"name": "Aarakocra", "classname": "Rogue", "level": 5, "spellslotlevel": None, "slots": None, "cantrips_known": None, "spells_known": None},
    {"name": "Aasimar", "classname": "Cleric", "level": 9, "spellslotlevel": None, "slots": None, "cantrips_known": None, "spells_known": None},
    {"name": "Vampire", "classname": "Paladin", "level": 8, "spellslotlevel": None, "slots": None, "cantrips_known": None, "spells_known": None},
    {"name": "Halfling", "classname": "Sorcerer", "level": 4, "spellslotlevel": None, "slots": None, "cantrips_known": None, "spells_known": None},
    {"name": "Dragonborn", "classname": "Warlock", "level": 6, "spellslotlevel": None, "slots": None, "cantrips_known": None, "spells_known": None}
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
    {"class": "Wizard", "subclass": "", "level": 20, "spellsknown": 44, "cantripsknown": 5},
    # Warlock spell and cantrip information
    {"class": "Warlock", "subclass": "", "level": 1, "spellsknown": 2, "cantripsknown": 2},
    {"class": "Warlock", "subclass": "", "level": 2, "spellsknown": 3, "cantripsknown": 2},
    {"class": "Warlock", "subclass": "", "level": 3, "spellsknown": 4, "cantripsknown": 2},
    {"class": "Warlock", "subclass": "", "level": 4, "spellsknown": 5, "cantripsknown": 3},
    {"class": "Warlock", "subclass": "", "level": 5, "spellsknown": 6, "cantripsknown": 3},
    {"class": "Warlock", "subclass": "", "level": 6, "spellsknown": 7, "cantripsknown": 3},
    {"class": "Warlock", "subclass": "", "level": 7, "spellsknown": 8, "cantripsknown": 3},
    {"class": "Warlock", "subclass": "", "level": 8, "spellsknown": 9, "cantripsknown": 3},
    {"class": "Warlock", "subclass": "", "level": 9, "spellsknown": 10, "cantripsknown": 3},
    {"class": "Warlock", "subclass": "", "level": 10, "spellsknown": 10, "cantripsknown": 4},
    {"class": "Warlock", "subclass": "", "level": 11, "spellsknown": 11, "cantripsknown": 4},
    {"class": "Warlock", "subclass": "", "level": 12, "spellsknown": 11, "cantripsknown": 4},
    {"class": "Warlock", "subclass": "", "level": 13, "spellsknown": 12, "cantripsknown": 4},
    {"class": "Warlock", "subclass": "", "level": 14, "spellsknown": 12, "cantripsknown": 4},
    {"class": "Warlock", "subclass": "", "level": 15, "spellsknown": 13, "cantripsknown": 4},
    {"class": "Warlock", "subclass": "", "level": 16, "spellsknown": 13, "cantripsknown": 4},
    {"class": "Warlock", "subclass": "", "level": 17, "spellsknown": 14, "cantripsknown": 4},
    {"class": "Warlock", "subclass": "", "level": 18, "spellsknown": 14, "cantripsknown": 4},
    {"class": "Warlock", "subclass": "", "level": 19, "spellsknown": 15, "cantripsknown": 4},
    {"class": "Warlock", "subclass": "", "level": 20, "spellsknown": 15, "cantripsknown": 4},
    # Sorcerer spell and cantrip information
    {"class": "Sorcerer", "subclass": "", "level": 1, "spellsknown": 2, "cantripsknown": 4},
    {"class": "Sorcerer", "subclass": "", "level": 2, "spellsknown": 3, "cantripsknown": 4},
    {"class": "Sorcerer", "subclass": "", "level": 3, "spellsknown": 4, "cantripsknown": 4},
    {"class": "Sorcerer", "subclass": "", "level": 4, "spellsknown": 5, "cantripsknown": 5},
    {"class": "Sorcerer", "subclass": "", "level": 5, "spellsknown": 6, "cantripsknown": 5},
    {"class": "Sorcerer", "subclass": "", "level": 6, "spellsknown": 7, "cantripsknown": 5},
    {"class": "Sorcerer", "subclass": "", "level": 7, "spellsknown": 8, "cantripsknown": 5},
    {"class": "Sorcerer", "subclass": "", "level": 8, "spellsknown": 9, "cantripsknown": 5},
    {"class": "Sorcerer", "subclass": "", "level": 9, "spellsknown": 10, "cantripsknown": 5},
    {"class": "Sorcerer", "subclass": "", "level": 10, "spellsknown": 11, "cantripsknown": 6},
    {"class": "Sorcerer", "subclass": "", "level": 11, "spellsknown": 12, "cantripsknown": 6},
    {"class": "Sorcerer", "subclass": "", "level": 12, "spellsknown": 12, "cantripsknown": 6},
    {"class": "Sorcerer", "subclass": "", "level": 13, "spellsknown": 13, "cantripsknown": 6},
    {"class": "Sorcerer", "subclass": "", "level": 14, "spellsknown": 13, "cantripsknown": 6},
    {"class": "Sorcerer", "subclass": "", "level": 15, "spellsknown": 14, "cantripsknown": 6},
    {"class": "Sorcerer", "subclass": "", "level": 16, "spellsknown": 14, "cantripsknown": 6},
    {"class": "Sorcerer", "subclass": "", "level": 17, "spellsknown": 15, "cantripsknown": 6},
    {"class": "Sorcerer", "subclass": "", "level": 18, "spellsknown": 15, "cantripsknown": 6},
    {"class": "Sorcerer", "subclass": "", "level": 19, "spellsknown": 15, "cantripsknown": 6},
    {"class": "Sorcerer", "subclass": "", "level": 20, "spellsknown": 15, "cantripsknown": 6},
    # Paladin spell and cantrip information
    {"class": "Paladin", "subclass": "", "level": 1, "spellsknown": 0, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 2, "spellsknown": 2, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 3, "spellsknown": 3, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 4, "spellsknown": 3, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 5, "spellsknown": 4, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 6, "spellsknown": 4, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 7, "spellsknown": 5, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 8, "spellsknown": 5, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 9, "spellsknown": 6, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 10, "spellsknown": 6, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 11, "spellsknown": 7, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 12, "spellsknown": 7, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 13, "spellsknown": 8, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 14, "spellsknown": 8, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 15, "spellsknown": 9, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 16, "spellsknown": 9, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 17, "spellsknown": 10, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 18, "spellsknown": 10, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 19, "spellsknown": 11, "cantripsknown": 0},
    {"class": "Paladin", "subclass": "", "level": 20, "spellsknown": 11, "cantripsknown": 0},
    # Cleric spell and cantrip information
    {"class": "Cleric", "subclass": "", "level": 1, "spellsknown": 0, "cantripsknown": 3},
    {"class": "Cleric", "subclass": "", "level": 2, "spellsknown": 0, "cantripsknown": 3},
    {"class": "Cleric", "subclass": "", "level": 3, "spellsknown": 0, "cantripsknown": 3},
    {"class": "Cleric", "subclass": "", "level": 4, "spellsknown": 0, "cantripsknown": 4},
    {"class": "Cleric", "subclass": "", "level": 5, "spellsknown": 0, "cantripsknown": 4},
    {"class": "Cleric", "subclass": "", "level": 6, "spellsknown": 0, "cantripsknown": 4},
    {"class": "Cleric", "subclass": "", "level": 7, "spellsknown": 0, "cantripsknown": 4},
    {"class": "Cleric", "subclass": "", "level": 8, "spellsknown": 0, "cantripsknown": 4},
    {"class": "Cleric", "subclass": "", "level": 9, "spellsknown": 0, "cantripsknown": 4},
    {"class": "Cleric", "subclass": "", "level": 10, "spellsknown": 0, "cantripsknown": 5},
    {"class": "Cleric", "subclass": "", "level": 11, "spellsknown": 0, "cantripsknown": 5},
    {"class": "Cleric", "subclass": "", "level": 12, "spellsknown": 0, "cantripsknown": 5},
    {"class": "Cleric", "subclass": "", "level": 13, "spellsknown": 0, "cantripsknown": 5},
    {"class": "Cleric", "subclass": "", "level": 14, "spellsknown": 0, "cantripsknown": 5},
    {"class": "Cleric", "subclass": "", "level": 15, "spellsknown": 0, "cantripsknown": 5},
    {"class": "Cleric", "subclass": "", "level": 16, "spellsknown": 0, "cantripsknown": 5},
    {"class": "Cleric", "subclass": "", "level": 17, "spellsknown": 0, "cantripsknown": 5},
    {"class": "Cleric", "subclass": "", "level": 18, "spellsknown": 0, "cantripsknown": 5},
    {"class": "Cleric", "subclass": "", "level": 19, "spellsknown": 0, "cantripsknown": 5},
    {"class": "Cleric", "subclass": "", "level": 20, "spellsknown": 0, "cantripsknown": 5}
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

# Display the final DataFrame
print(df_characters)
df_characters.to_csv('characters.csv', index=False)
