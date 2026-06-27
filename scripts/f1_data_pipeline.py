"""
Formula 1 Race Analytics - ETL Pipeline
Extracts race data from FastF1 API, transforms, and loads to analysis-ready format
Demonstrates: API Integration, ETL, Data Pipeline, Python, Pandas
"""
import fastf1
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from pathlib import Path

# Enable caching for faster subsequent loads
fastf1.Cache.enable_cache('data/cache')

class F1DataPipeline:
    """ETL pipeline for Formula 1 race data extraction"""

    def __init__(self, season=2024):
        self.season = season
        self.raw_data_dir = Path('data/raw')
        self.processed_data_dir = Path('data/processed')
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)

    def extract_race_schedule(self):
        """Extract race schedule for the season"""
        print(f"Extracting {self.season} race schedule...")
        schedule = fastf1.get_event_schedule(self.season)

        # Save raw data
        schedule.to_csv(self.raw_data_dir / f'schedule_{self.season}.csv', index=False)
        print(f"  ✓ Saved {len(schedule)} races")
        return schedule

    def extract_race_results(self, round_number, event_name):
        """Extract results for a specific race"""
        try:
            print(f"Extracting Round {round_number}: {event_name}...")
            session = fastf1.get_session(self.season, round_number, 'R')  # 'R' = Race
            session.load()

            # Extract results
            results = session.results
            if results is not None and len(results) > 0:
                results['season'] = self.season
                results['round'] = round_number
                results['event_name'] = event_name

                # Save raw
                filename = f'results_{self.season}_r{round_number}.csv'
                results.to_csv(self.raw_data_dir / filename, index=False)
                print(f"  ✓ Saved {len(results)} driver results")
                return results
            else:
                print(f"  ⚠ No results available")
                return None

        except Exception as e:
            print(f"  ✗ Error: {e}")
            return None

    def extract_lap_data(self, round_number, event_name):
        """Extract lap-by-lap timing data"""
        try:
            print(f"Extracting lap data for Round {round_number}...")
            session = fastf1.get_session(self.season, round_number, 'R')
            session.load()

            laps = session.laps
            if laps is not None and len(laps) > 0:
                laps['season'] = self.season
                laps['round'] = round_number
                laps['event_name'] = event_name

                filename = f'laps_{self.season}_r{round_number}.csv'
                laps.to_csv(self.raw_data_dir / filename, index=False)
                print(f"  ✓ Saved {len(laps)} lap records")
                return laps
            else:
                print(f"  ⚠ No lap data available")
                return None

        except Exception as e:
            print(f"  ✗ Error: {e}")
            return None

    def transform_results(self, results_df):
        """Transform raw results into analysis-ready format"""
        if results_df is None or len(results_df) == 0:
            return None

        df = results_df.copy()

        # Select and rename key columns
        columns_of_interest = [
            'DriverNumber', 'BroadcastName', 'Abbreviation', 'TeamName',
            'Position', 'GridPosition', 'Time', 'Status', 'Points',
            'season', 'round', 'event_name'
        ]

        # Keep only available columns
        available_cols = [c for c in columns_of_interest if c in df.columns]
        df = df[available_cols]

        # Data cleaning
        df['Position'] = pd.to_numeric(df['Position'], errors='coerce')
        df['GridPosition'] = pd.to_numeric(df['GridPosition'], errors='coerce')
        df['Points'] = pd.to_numeric(df['Points'], errors='coerce')

        # Calculate positions gained/lost
        if 'Position' in df.columns and 'GridPosition' in df.columns:
            df['PositionsGained'] = df['GridPosition'] - df['Position']

        # Handle missing values
        df['Points'] = df['Points'].fillna(0)

        return df

    def transform_lap_data(self, laps_df):
        """Transform lap data for analysis"""
        if laps_df is None or len(laps_df) == 0:
            return None

        df = laps_df.copy()

        # Convert lap times to seconds
        if 'LapTime' in df.columns:
            df['LapTimeSeconds'] = df['LapTime'].dt.total_seconds()

        # Calculate sector times if available
        for sector in [1, 2, 3]:
            col = f'Sector{sector}Time'
            if col in df.columns:
                df[f'Sector{sector}Seconds'] = df[col].dt.total_seconds()

        # Driver performance metrics
        df['IsPersonalBest'] = df.get('IsPersonalBest', False)

        return df

    def load_to_processed(self, df, filename):
        """Load transformed data to processed directory"""
        if df is not None and len(df) > 0:
            filepath = self.processed_data_dir / filename
            df.to_csv(filepath, index=False)
            print(f"  ✓ Loaded {len(df)} records to {filename}")
            return filepath
        return None

    def run_pipeline(self, max_races=5):
        """Run full ETL pipeline"""
        print("=" * 60)
        print(f"F1 DATA PIPELINE - {self.season} Season")
        print("=" * 60)

        # Extract schedule
        schedule = self.extract_race_schedule()

        # Process first N races
        races_processed = 0
        for idx, race in schedule.head(max_races).iterrows():
            round_num = race['RoundNumber']
            event_name = race['EventName']

            # Extract
            results = self.extract_race_results(round_num, event_name)
            laps = self.extract_lap_data(round_num, event_name)

            # Transform
            results_clean = self.transform_results(results)
            laps_clean = self.transform_lap_data(laps)

            # Load
            if results_clean is not None:
                self.load_to_processed(results_clean, f'results_r{round_num}_clean.csv')
            if laps_clean is not None:
                self.load_to_processed(laps_clean, f'laps_r{round_num}_clean.csv')

            races_processed += 1

        print("
" + "=" * 60)
        print(f"PIPELINE COMPLETE: {races_processed} races processed")
        print("=" * 60)

        # Generate summary report
        self.generate_summary()

    def generate_summary(self):
        """Generate data quality summary"""
        print("\n📊 DATA QUALITY SUMMARY")
        print("-" * 40)

        raw_files = list(self.raw_data_dir.glob('*.csv'))
        processed_files = list(self.processed_data_dir.glob('*.csv'))

        print(f"Raw data files: {len(raw_files)}")
        print(f"Processed files: {len(processed_files)}")

        total_raw_rows = 0
        total_processed_rows = 0

        for f in raw_files:
            df = pd.read_csv(f)
            total_raw_rows += len(df)

        for f in processed_files:
            df = pd.read_csv(f)
            total_processed_rows += len(df)

        print(f"Total raw records: {total_raw_rows}")
        print(f"Total processed records: {total_processed_rows}")
        print(f"Data retention rate: {total_processed_rows/max(total_raw_rows,1)*100:.1f}%")

def main():
    """Main execution"""
    pipeline = F1DataPipeline(season=2024)
    pipeline.run_pipeline(max_races=3)  # Process first 3 races for demo

if __name__ == '__main__':
    main()
