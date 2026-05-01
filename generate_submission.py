import json
from bot import compose

# Load data
with open("dataset/categories/dentists.json") as f:
    category = json.load(f)

with open("dataset/merchants_seed.json") as f:
    merchants = json.load(f)["merchants"]

with open("dataset/triggers_seed.json") as f:
    triggers = json.load(f)["triggers"]

output = []

# Generate 30 test cases (simple version)
for i in range(30):
    merchant = merchants[i % len(merchants)]
    trigger = triggers[i % len(triggers)]

    result = compose(category, merchant, trigger)

    output.append({
        "test_id": f"T{i+1:02}",
        "body": result["body"],
        "cta": result["cta"],
        "send_as": result["send_as"],
        "suppression_key": result["suppression_key"],
        "rationale": result["rationale"]
    })

# Save file
with open("submission.jsonl", "w") as f:
    for row in output:
        f.write(json.dumps(row) + "\n")

print("✅ submission.jsonl created")