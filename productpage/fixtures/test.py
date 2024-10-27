import json
import uuid

# Load your existing JSON data
with open('./product_data.json', 'r') as file:
    data = json.load(file)

# Update the pk for each Toko entry
for entry in data:
    if entry['model'] == 'storepage.Toko':
        entry['pk'] = str(uuid.uuid4())

# Save the updated data back to a JSON file
with open('updated_fixture_file.json', 'w') as file:
    json.dump(data, file, indent=4)