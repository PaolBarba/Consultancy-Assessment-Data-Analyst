import numpy as np
import pandas as pd


def get_most_recent(row, year_cols):
    """
    Return the most recent non-NA value from the given row for the specified year columns.

    Parameters
    ----------
    row : pandas.Series
        The row of data to search.
    year_cols : list
        List of column names (years) to check in order.

    Returns
    -------
    The first non-NA value found in the specified columns, or np.nan if none are found.
    """
    for year in year_cols:
        value = row[year]
        if pd.notna(value):
            return value
    return np.nan
