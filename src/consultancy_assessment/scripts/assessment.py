"""Consultancy Assessment Module."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from consultancy_assessment.scripts.file_loader import FileLoader
from consultancy_assessment.utils import get_most_recent


class ConsultancyAssessment:
    """A class for managing consultancy assessments."""

    def __init__(self):
        self.file_loader = FileLoader()

    def load_global_data_flow(self, global_data_flow_file_path):
        """Load datasets: on_track_of_track, world_population_prospect, and global_data_flow."""
        self.on_track_of_track = self.file_loader.load(self.file_loader.on_track_of_track_file_path)
        self.world_population_prospect = self.file_loader.load(self.file_loader.world_population_prospect_file_path)
        self.global_data_flow = self.file_loader.load(global_data_flow_file_path)

    def clean_on_track_of_track(self):
        """Standardize and clean Status.U5MR values."""
        status_map = {
            "achieved": "On-track",
            "on track": "On-track",
            "acceleration needed": "Off-track"
        }
        self.on_track_of_track["Status.U5MR"] = (
            self.on_track_of_track["Status.U5MR"]
            .str.lower()
            .map(status_map)
            .fillna(self.on_track_of_track["Status.U5MR"])
        )

    def clean_global_data_flow(self):
        """Standardize global data flow format and remove incomplete rows."""
        self.global_data_flow.columns = self.global_data_flow.iloc[0]
        self.global_data_flow = self.global_data_flow[1:].reset_index(drop=True)
        self.global_data_flow = self.global_data_flow[
            self.global_data_flow["Geographic area"].notna() &
            self.global_data_flow["Indicator"].notna()
        ]
        self.global_data_flow.columns = ["Geographic area", "Indicator", "Sex", "2022", "2021", "2020", "2019", "2018"]

    def add_most_recent_estimate(self):
        """Add a column with the most recent available estimate."""
        self.global_data_flow.replace("-", np.nan, inplace=True)
        year_cols = [col for col in self.global_data_flow.columns if str(col).isdigit()]
        year_cols = sorted(year_cols, reverse=True)
        self.global_data_flow["most_recent_estimate"] = self.global_data_flow.apply(
            get_most_recent, axis=1, year_cols=year_cols
        )

    def merge_datasets(self):
        """Merge all datasets into a single DataFrame."""
        merged = self.on_track_of_track.merge(
            self.world_population_prospect,
            left_on="ISO3Code",
            right_on="ISO3 Alpha-code",
            how="inner"
        )

        merged = merged.merge(
            self.global_data_flow,
            left_on="OfficialName",
            right_on="Geographic area",
            how="inner"
        )

        # Rename columns for clarity
        merged = merged.rename(columns={
            "most_recent_estimate": "MostRecentEstimate",
            "Indicator": "Indicator",
            "Births (thousands)": "BirthsThousands"
        })

        # Ensure numeric types
        merged["MostRecentEstimate"] = pd.to_numeric(merged["MostRecentEstimate"], errors="coerce")
        merged["BirthsThousands"] = pd.to_numeric(merged["BirthsThousands"], errors="coerce")

        self.merged_data = merged

    def compute_population_weighted_coverage(self):
        """Compute population-weighted coverage grouped by Status and Indicator."""
        result = (
            self.merged_data
            .groupby(["Status.U5MR", "Indicator"], group_keys=False)
            .apply(lambda x: np.average(x["MostRecentEstimate"], weights=x["BirthsThousands"]))
            .reset_index(name="PopulationWeightedCoverage")
        )
        result["PopulationWeightedCoverage"] = result["PopulationWeightedCoverage"].round(2)
        return result

    def plot_output(self, data):
        """Plot the weighted coverage by status and indicator in a more beautiful style."""
        # Set the seaborn theme
        sns.set_theme(style="whitegrid")

        # Set figure size
        plt.figure(figsize=(12, 7))

        # Use a modern color palette sized to the number of unique indicators
        unique_indicators = data["Indicator"].nunique()
        palette = sns.color_palette("Set2", n_colors=unique_indicators)

        # Create the barplot
        sns.barplot(
            x="Status.U5MR",
            y="PopulationWeightedCoverage",
            hue="Indicator",
            data=data,
            edgecolor="black",
            palette=palette
        )

        # Titles and labels
        plt.title("Population Weighted Coverage by U5MR Status and Indicator", fontsize=16, weight="bold")
        plt.xlabel("U5MR Status", fontsize=13)
        plt.ylabel("Coverage (Population Weighted)", fontsize=13)

        # Tweak ticks
        plt.xticks(fontsize=11)
        plt.yticks(fontsize=11)

        # Add gridlines
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # Add legend with title
        plt.legend(title="Indicator", title_fontsize=12, fontsize=11)

        # Tight layout
        plt.tight_layout()
        # Save the plot
        output_path = Path("src/consultancy_assessment/documentation/population_weighted_coverage.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
        plt.close()
        return

    def run(self):
        """Run the full consultancy assessment pipeline."""
        self.load_global_data_flow(self.file_loader.global_data_flow_file_path)
        self.clean_global_data_flow()
        self.clean_on_track_of_track()
        self.add_most_recent_estimate()
        self.merge_datasets()
        data = self.compute_population_weighted_coverage()
        self.plot_output(data)
        return data
