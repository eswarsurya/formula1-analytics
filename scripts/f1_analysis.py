"""
Formula 1 Race Analytics - Analysis & Visualization
Demonstrates: Data Analysis, Python, Pandas, Data Visualization
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class F1Analyzer:
    """Analyze Formula 1 race data"""

    def __init__(self, data_dir='data/processed'):
        self.data_dir = Path(data_dir)
        self.results = []
        self.laps = []
        self._load_data()

    def _load_data(self):
        """Load all processed data"""
        for f in self.data_dir.glob('results_*_clean.csv'):
            df = pd.read_csv(f)
            self.results.append(df)

        for f in self.data_dir.glob('laps_*_clean.csv'):
            df = pd.read_csv(f)
            self.laps.append(df)

        if self.results:
            self.results_df = pd.concat(self.results, ignore_index=True)
            print(f"Loaded {len(self.results_df)} result records")
        else:
            self.results_df = pd.DataFrame()

        if self.laps:
            self.laps_df = pd.concat(self.laps, ignore_index=True)
            print(f"Loaded {len(self.laps_df)} lap records")
        else:
            self.laps_df = pd.DataFrame()

    def driver_standings(self):
        """Calculate driver championship standings"""
        if self.results_df.empty:
            print("No results data available")
            return

        standings = self.results_df.groupby('Abbreviation').agg({
            'Points': 'sum',
            'Position': 'mean',
            'PositionsGained': 'sum'
        }).round(2)

        standings = standings.sort_values('Points', ascending=False)
        standings['Rank'] = range(1, len(standings) + 1)

        print("\n🏆 DRIVER STANDINGS")
        print("-" * 50)
        print(standings.head(10))

        return standings

    def team_performance(self):
        """Analyze team performance"""
        if self.results_df.empty or 'TeamName' not in self.results_df.columns:
            print("No team data available")
            return

        team_stats = self.results_df.groupby('TeamName').agg({
            'Points': 'sum',
            'Position': 'mean'
        }).round(2)

        team_stats = team_stats.sort_values('Points', ascending=False)

        print("\n🏎️ TEAM PERFORMANCE")
        print("-" * 50)
        print(team_stats)

        return team_stats

    def qualifying_vs_race(self):
        """Analyze qualifying vs race performance"""
        if self.results_df.empty:
            return

        df = self.results_df.dropna(subset=['GridPosition', 'Position'])

        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='GridPosition', y='Position', hue='TeamName', s=100)
        plt.plot([1, 20], [1, 20], 'r--', alpha=0.5, label='Perfect correlation')
        plt.xlabel('Qualifying Position')
        plt.ylabel('Race Finish Position')
        plt.title('Qualifying vs Race Performance')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig('notebooks/qualifying_vs_race.png', dpi=300, bbox_inches='tight')
        print("\n📈 Saved: notebooks/qualifying_vs_race.png")
        plt.close()

    def positions_gained_analysis(self):
        """Analyze who gains most positions during race"""
        if self.results_df.empty or 'PositionsGained' not in self.results_df.columns:
            return

        df = self.results_df.dropna(subset=['PositionsGained'])

        avg_gains = df.groupby('Abbreviation')['PositionsGained'].mean().sort_values(ascending=False)

        plt.figure(figsize=(12, 6))
        avg_gains.head(15).plot(kind='bar', color='steelblue')
        plt.title('Average Positions Gained per Race')
        plt.xlabel('Driver')
        plt.ylabel('Positions Gained')
        plt.axhline(y=0, color='red', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('notebooks/positions_gained.png', dpi=300, bbox_inches='tight')
        print("📈 Saved: notebooks/positions_gained.png")
        plt.close()

        return avg_gains

    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "=" * 60)
        print("FORMULA 1 RACE ANALYTICS REPORT")
        print("=" * 60)

        self.driver_standings()
        self.team_performance()
        self.qualifying_vs_race()
        self.positions_gained_analysis()

        print("\n" + "=" * 60)
        print("REPORT GENERATION COMPLETE")
        print("=" * 60)

def main():
    analyzer = F1Analyzer()
    analyzer.generate_report()

if __name__ == '__main__':
    main()
