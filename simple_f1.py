import fastf1
import pandas as pd

# Enable cache
fastf1.Cache.enable_cache('cache')

# Get 2024 Bahrain GP
session = fastf1.get_session(2024, 1, 'R')
session.load()

# Get results
results = session.results
print(f"Loaded {len(results)} driver results")

# Save to CSV
results.to_csv('bahrain_2024.csv', index=False)
print("Saved to bahrain_2024.csv")