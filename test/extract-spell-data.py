import json
import pandas as pd

# Load the JSON file with utf-8-sig encoding to handle BOM
file_path = "./classes.json"
with open(file_path, "r", encoding="utf-8-sig") as file:
    data = json.load(file)

# Extract relevant data: classTableGroups for each class with spells known and cantrips known
extracted_data = []
for class_data in data["class"]:
    class_name = class_data["name"]
    for group in class_data["classTableGroups"]:
        if any(label in group["colLabels"] for label in ["Cantrips Known", "Spells Known", "Spells Prepared"]):
            subclass_name = None
            for label in group["colLabels"]:
                if "subclass" in label:
                    subclass_name = label.split("subclass ")[-1]
                    break
            for level, row in enumerate(group["rows"], start=1):
                cantrips_known = spells_known = None
                for label, value in zip(group["colLabels"], row):
                    if "Cantrips Known" in label:
                        cantrips_known = value
                    elif "Spells Known" in label or "Spells Prepared" in label:
                        spells_known = value
                extracted_data.append({
                    "class": class_name,
                    "subclass": subclass_name if subclass_name else "",
                    "level": level,
                    "spellsknown": spells_known,
                    "cantripsknown": cantrips_known
                })

# Convert to DataFrame for better readability
df = pd.DataFrame(extracted_data)

# Save to CSV
output_file_path = "./spells-known.csv"
df.to_csv(output_file_path, index=False)

print(f"Data successfully extracted and saved to {output_file_path}")
