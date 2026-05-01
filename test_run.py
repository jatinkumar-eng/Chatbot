import json
from bot import compose

# -------- Load category --------
with open("dataset/categories/dentists.json") as f:
    category = json.load(f)

# -------- Load merchant --------
with open("dataset/merchants_seed.json") as f:
    merchants = json.load(f)

merchant = merchants["merchants"][0]   # ✅ FIXED

# -------- Load trigger --------
with open("dataset/triggers_seed.json") as f:
    triggers = json.load(f)

trigger = triggers["triggers"][0]      # ✅ FIXED

# -------- Run bot --------
result = compose(category, merchant, trigger)

print(result)