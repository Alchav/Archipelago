import json
import re

# Load JSON data
with open('data/regions.json', 'r') as f:
    data = json.load(f)


with open('rules.py', 'r') as f:
    lines = f.readlines()

events = []

for line in lines:
    # Look for event names in the line
    matches = re.findall(r'"(EVENT_[A-Z_]+)"', line)
    # Append found event names to the list
    events.extend(matches)

# Iterate through each entry in the JSON data
for region, details in data.items():
    # Remove specific events from the "events" list
    details["events"] = [event for event in details["events"]
                         if event in events]

# Print the updated JSON data (optional)
# print(json.dumps(data, indent=4))

# Optionally, you can write the updated data back to the file
with open('data/regions.json', 'w') as f:
    json.dump(data, f, indent=4)
