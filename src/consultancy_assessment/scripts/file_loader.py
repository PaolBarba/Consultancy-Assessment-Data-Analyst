

import yaml
from matplotlib.path import Path
import pandas as pd

class FileLoader:
    """FileLoader class to handle loading of datasets."""

    def __init__(self):
        self.config = self.load_config_yaml("src/consultancy_assessment/user_profile.yaml")
        self.global_data_flow_file_path = self.config.get("global_dataflow_file_path", "")
        self.on_track_of_track_file_path = self.config.get("raw_data_file_path", [])[0]
        self.world_population_prospect_file_path = self.config.get("raw_data_file_path", [])[1]

    def load_config_yaml(self, file_path):
        """Load a YAML configuration file."""
        with open(file_path) as file:
            return yaml.safe_load(file)

    def load(self, file_path):
        """
        Load a dataset from a given file path.

        Parameters
        ----------
        file_path : str
            The path to the file to be loaded.

        Returns
        -------
        DataFrame or None
            The loaded data as a pandas DataFrame, or None if the file type is unsupported.
        """
        if file_path.endswith(".xlsx"):
            # if the file is WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1 skip the first 16 rows
            if "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1" in file_path:
                return pd.read_excel(file_path, skiprows=16)
            return pd.read_excel(file_path)
        return None
