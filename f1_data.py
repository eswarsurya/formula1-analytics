import fastf1
import pandas as pd
import os

# Cache setup
script_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(script_dir, 'cache')
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

# Get schedule
schedule = fastf1.get_event_schedule(2026)

# Get only completed races
completed = schedule[schedule['EventDate'] < pd.Timestamp.today()]

# Get latest race
latest_event = completed.iloc[-1]

year = latest_event['EventDate'].year
round_number = latest_event['RoundNumber']

print(f"Latest race round: {round_number}")

# Load latest race
session = fastf1.get_session(year, round_number, 'R')
session.load()

# Get results
results = session.results

# Race info
race_name = latest_event['EventName']
race_date = latest_event['EventDate']
circuit = latest_event['Location']

# Prepare dataframe
results_clean = results[['DriverNumber', 'Abbreviation', 'Position', 'Points']].copy()
results_clean['RaceName'] = race_name
results_clean['RaceDate'] = race_date
results_clean['Circuit'] = circuit

# Save
csv_path = os.path.join(script_dir, 'f1_results.csv')
results_clean.to_csv(csv_path, index=False)

print("✅ Latest race data updated!")