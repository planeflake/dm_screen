// Create or update Rogue Class Node with properties
MERGE (c:Class {name: "Rogue"})
ON CREATE SET 
    c.hd_number = 1, 
    c.hd_faces = 8, 
    c.proficiency = ["dex", "int"], 
    c.description = "A scoundrel who uses stealth and trickery to overcome obstacles and enemies.",
    c.page = 94,
    c.source = "PHB"
ON MATCH SET 
    c.proficiency = ["dex", "int"], 
    c.description = "A scoundrel who uses stealth and trickery to overcome obstacles and enemies.",
    c.page = 94,
    c.source = "PHB"

WITH c
// Add starting proficiencies as a new node
MERGE (sp:StartingProficiencies {class: "Rogue"})
ON CREATE SET sp.armor = ["light"],
              sp.tools = ["thieves' tools"],
              sp.skills_choice_count = 4
MERGE (c)-[:HAS_STARTING_PROFICIENCIES]->(sp)

// Link starting proficiency skills to Skill nodes
WITH c, sp
UNWIND ["acrobatics", "athletics", "deception", "insight", "intimidation", "investigation", "perception", "performance", "persuasion", "sleight of hand", "stealth"] AS skillName
MERGE (skill:Skill {name: skillName})
MERGE (sp)-[:CAN_CHOOSE_SKILL_FROM]->(skill)

// Link starting proficiency weapons to Weapon nodes
WITH c, sp
UNWIND ["simple", "hand crossbow", "longsword", "rapier", "shortsword"] AS weaponName
MERGE (weapon:Weapon {name: weaponName})
MERGE (sp)-[:CAN_USE_WEAPON]->(weapon)

// Add starting equipment as a new node
MERGE (se:StartingEquipment {class: "Rogue"})
ON MATCH SET se.additionalFromBackground = true,
              se.default = apoc.convert.toJson(["(a) a rapier or (b) a shortsword", "(a) a shortbow and quiver of 20 arrows or (b) a shortsword", "(a) a burglar's pack, (b) a dungeoneer's pack, or (c) an explorer's pack", "Leather armor, two daggers, and thieves' tools"]),
              se.goldAlternative = "4d4 × 10"
MERGE (c)-[:HAS_STARTING_EQUIPMENT]->(se)

// Add multiclassing as a new node
MERGE (mc:Multiclassing {class: "Rogue"})
ON MATCH SET mc.requirements = apoc.convert.toJson({dex: 13})
MERGE (c)-[:HAS_MULTICLASSING]->(mc)

// Link multiclassing proficiencies to Skill nodes
WITH c, mc
UNWIND ["acrobatics", "athletics", "deception", "insight", "intimidation", "investigation", "perception", "performance", "persuasion", "sleight of hand", "stealth"] AS multiSkillName
MERGE (multiSkill:Skill {name: multiSkillName})
MERGE (mc)-[:CAN_CHOOSE_SKILL_FROM]->(multiSkill)

// Link multiclassing proficiencies to Weapon nodes
WITH c, mc
UNWIND ["light"] AS multiWeaponName
MERGE (multiWeapon:Weapon {name: multiWeaponName})
MERGE (mc)-[:CAN_USE_WEAPON]->(multiWeapon)

// Link Class to Source
WITH c
MATCH (s:Source {abbrev: "PHB"})
MERGE (c)-[:FROM_SOURCE]->(s)

// Create Subclass Nodes and Relationships
WITH c
UNWIND [
    {name: "Arcane Trickster", shortName: "Arcane Trickster", source: "PHB", page: 97, spellcastingAbility: "int", casterProgression: "1/3", cantripProgression: [0, 0, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], spellsKnownProgression: [0, 0, 3, 4, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11, 11, 11, 12, 13], additionalSpells: apoc.map.fromValues(["3", ["mage hand"]]), subclassFeatures: ["Arcane Trickster|Rogue||Arcane Trickster||3", "Magical Ambush|Rogue||Arcane Trickster||9", "Versatile Trickster|Rogue||Arcane Trickster||13", "Spell Thief|Rogue||Arcane Trickster||17"]},
    {name: "Assassin", shortName: "Assassin", source: "PHB", page: 97, subclassFeatures: ["Assassin|Rogue||Assassin||3", "Infiltration Expertise|Rogue||Assassin||9", "Impostor|Rogue||Assassin||13", "Death Strike|Rogue||Assassin||17"]},
    {name: "Thief", shortName: "Thief", source: "PHB", page: 97, subclassFeatures: ["Thief|Rogue||Thief||3", "Supreme Sneak|Rogue||Thief||9", "Use Magic Device|Rogue||Thief||13", "Thief's Reflexes|Rogue||Thief||17"]}
] AS subclassData

WITH c, subclassData
MERGE (sc:Subclass {name: subclassData.name, source: subclassData.source})
ON CREATE SET sc.shortName = subclassData.shortName, sc.page = subclassData.page, sc.spellcastingAbility = subclassData.spellcastingAbility, sc.casterProgression = subclassData.casterProgression
MERGE (c)-[:HAS_SUBCLASS]->(sc)

WITH c,sc, subclassData
MATCH (s:Source {abbrev: subclassData.source})
MERGE (sc)-[:FROM_SOURCE]->(s)

// Create Subclass Features Nodes
WITH c,sc, subclassData
UNWIND subclassData.subclassFeatures AS sf
WITH c,sc, split(sf, '|') AS parts
MERGE (sfNode:Feature {name: parts[0], level: parts[-1]})
MERGE (sc)-[:HAS_FEATURE]->(sfNode)

// Create Class Features Nodes and Relationships
WITH c,sc
UNWIND [
    {classFeature: "Expertise|Rogue||1", description: "At 1st level, choose two of your skill proficiencies, or one of your skill proficiencies and your proficiency with thieves' tools. Your proficiency bonus is doubled for any ability check you make that uses either of the chosen proficiencies."},
    {classFeature: "Sneak Attack|Rogue||1", description: "Beginning at 1st level, you know how to strike subtly and exploit a foe's distraction. Once per turn, you can deal an extra 1d6 damage to one creature you hit with an attack if you have advantage on the attack roll. The attack must use a finesse or a ranged weapon."},
    {classFeature: "Thieves' Cant|Rogue||1", description: "During your rogue training you learned thieves' cant, a secret mix of dialect, jargon, and code that allows you to hide messages in seemingly normal conversation. Only another creature that knows thieves' cant understands such messages."},
    {classFeature: "Cunning Action|Rogue||2", description: "Starting at 2nd level, your quick thinking and agility allow you to move and act quickly. You can take a bonus action on each of your turns in combat. This action can be used only to take the Dash, Disengage, or Hide action."},
    {classFeature: "Cunning Action: Aim|Rogue||2|UAClassFeatureVariants", description: "As a bonus action, you give yourself advantage on your next attack roll on the current turn. You can use this bonus action only if you haven’t moved during this turn, and after you use the bonus action, your speed is 0 until the end of the current turn."},
    {classFeature: "Roguish Archetype|Rogue||3", description: "At 3rd level, you choose an archetype that you emulate in the exercise of your rogue abilities.", gainSubclassFeature: true},
    {classFeature: "Steady Aim|Rogue||3|TCE", description: "As a bonus action, you give yourself advantage on your next attack roll on the current turn. You can use this bonus action only if you haven’t moved during this turn, and after you use the bonus action, your speed is 0 until the end of the current turn."},
    {classFeature: "Ability Score Improvement|Rogue||4", description: "When you reach 4th level, and again at 8th, 10th, 12th, 16th, and 19th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can’t increase an ability score above 20 using this feature."},
    {classFeature: "Proficiency Versatility|Rogue||4|UAClassFeatureVariants", description: "Whenever you gain the Ability Score Improvement feature from your class, you can replace one of your skill proficiencies with a skill proficiency offered by your class at 1st level."},
    {classFeature: "Uncanny Dodge|Rogue||5", description: "Starting at 5th level, when an attacker that you can see hits you with an attack, you can use your reaction to halve the attack’s damage against you."},
    {classFeature: "Expertise|Rogue||6", description: "At 6th level, choose two more of your proficiencies in skills, or one of your proficiencies in skills and your proficiency with thieves' tools. Your proficiency bonus is doubled for any ability check you make that uses either of the chosen proficiencies."},
    {classFeature: "Evasion|Rogue||7", description: "Beginning at 7th level, you can nimbly dodge out of the way of certain area effects, such as a red dragon’s fiery breath or an ice storm spell. When you are subjected to an effect that allows you to make a Dexterity saving throw to take only half damage, you instead take no damage if you succeed on the saving throw, and only half damage if you fail."},
    {classFeature: "Ability Score Improvement|Rogue||8", description: "When you reach 8th level, and again at 10th, 12th, 16th, and 19th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can’t increase an ability score above 20 using this feature."},
    {classFeature: "Proficiency Versatility|Rogue||8|UAClassFeatureVariants", description: "Whenever you gain the Ability Score Improvement feature from your class, you can replace one of your skill proficiencies with a skill proficiency offered by your class at 1st level."},
    {classFeature: "Roguish Archetype feature|Rogue||9", description: "At 9th level, you gain a feature granted by your Roguish Archetype.", gainSubclassFeature: true},
    {classFeature: "Ability Score Improvement|Rogue||10", description: "When you reach 10th level, and again at 12th, 16th, and 19th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can’t increase an ability score above 20 using this feature."},
    {classFeature: "Proficiency Versatility|Rogue||10|UAClassFeatureVariants", description: "Whenever you gain the Ability Score Improvement feature from your class, you can replace one of your skill proficiencies with a skill proficiency offered by your class at 1st level."},
    {classFeature: "Reliable Talent|Rogue||11", description: "By 11th level, you have refined your chosen skills until they approach perfection. Whenever you make an ability check that lets you add your proficiency bonus, you can treat a d20 roll of 9 or lower as a 10."},
    {classFeature: "Ability Score Improvement|Rogue||12", description: "When you reach 12th level, and again at 16th and 19th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can’t increase an ability score above 20 using this feature."},
    {classFeature: "Proficiency Versatility|Rogue||12|UAClassFeatureVariants", description: "Whenever you gain the Ability Score Improvement feature from your class, you can replace one of your skill proficiencies with a skill proficiency offered by your class at 1st level."},
    {classFeature: "Roguish Archetype feature|Rogue||13", description: "At 13th level, you gain a feature granted by your Roguish Archetype.", gainSubclassFeature: true},
    {classFeature: "Blindsense|Rogue||14", description: "Starting at 14th level, if you are able to hear, you are aware of the location of any hidden or invisible creature within 10 feet of you."},
    {classFeature: "Slippery Mind|Rogue||15", description: "By 15th level, you have acquired greater mental strength. You gain proficiency in Wisdom saving throws."},
    {classFeature: "Ability Score Improvement|Rogue||16", description: "When you reach 16th level, and again at 19th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can’t increase an ability score above 20 using this feature."},
    {classFeature: "Proficiency Versatility|Rogue||16|UAClassFeatureVariants", description: "Whenever you gain the Ability Score Improvement feature from your class, you can replace one of your skill proficiencies with a skill proficiency offered by your class at 1st level."},
    {classFeature: "Roguish Archetype feature|Rogue||17", description: "At 17th level, you gain a feature granted by your Roguish Archetype.", gainSubclassFeature: true},
    {classFeature: "Elusive|Rogue||18", description: "Beginning at 18th level, you are so evasive that attackers rarely gain the upper hand against you. No attack roll has advantage against you while you aren’t incapacitated."},
    {classFeature: "Ability Score Improvement|Rogue||19", description: "When you reach 19th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can’t increase an ability score above 20 using this feature."},
    {classFeature: "Proficiency Versatility|Rogue||19|UAClassFeatureVariants", description: "Whenever you gain the Ability Score Improvement feature from your class, you can replace one of your skill proficiencies with a skill proficiency offered by your class at 1st level."},
    {classFeature: "Stroke of Luck|Rogue||20", description: "At 20th level, you have an uncanny knack for succeeding when you need to. If your attack misses a target within range, you can turn the miss into a hit. Alternatively, if you fail an ability check, you can treat the d20 roll as a 20. Once you use this feature, you can’t use it again until you finish a short or long rest."}
] AS featureData

WITH c,sc, featureData
UNWIND featureData AS feature
WITH c,sc, split(feature.classFeature, '|') AS parts, feature, featureData
MERGE (f:Feature {name: parts[0], level: parts[-1]})
ON MATCH SET f.description = feature.description
MERGE (c)-[:HAS_FEATURE]->(f)

// Create relationships for subclass features
WITH c,sc, featureData
UNWIND featureData AS feature
WITH sc, split(feature.classFeature, '|') AS parts, feature
FOREACH (gain IN CASE WHEN feature.gainSubclassFeature THEN [1] ELSE [] END | 
    MERGE (f:Feature {name: parts[0], level: parts[-1]})
    MERGE (sc)-[:GRANTS_FEATURE]->(f)
)
