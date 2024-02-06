from pprint import pprint
from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew


def read_excel_to_series(file_path: str) -> pd.DataFrame:
    """
    Reads an Excel file into a Pandas Series.

    Parameters:
    - file_path (str): Path to the Excel file.

    Returns:
    - pd.Series: Pandas Series containing the data.
    """
    df = pd.read_excel(io=file_path)
    df = df.dropna(subset=["Spread"])
    return df


def strip_data(df: pd.Series, column: str) -> np.ndarray:
    """
    Converts a Pandas Series to a NumPy array.

    Parameters:
    - series (pd.Series): Pandas Series to be converted.

    Returns:
    - np.ndarray: NumPy array containing the data.
    """
    try:
        df = df[column].values
        return df
    except Exception as e:
        print(f"Error converting Series to NumPy array: {e}")
        return []


def series_to_numpy(series: pd.Series, column: str) -> np.ndarray:
    """
    Converts a Pandas Series to a NumPy array.

    Parameters:
    - series (pd.Series): Pandas Series to be converted.

    Returns:
    - np.ndarray: NumPy array containing the data.
    """
    try:
        series = series[column]
        numpy_array = series.to_numpy()
        return numpy_array
    except Exception as e:
        print(f"Error converting Series to NumPy array: {e}")
        return np.array([])


def mean_squared_error(x_1: np.ndarray, x_2: np.ndarray) -> float:
    """
    Calculate the Mean Squared Error (MSE) between observed and predicted values.

    Parameters:
    - observed: List or array of observed values.
    - predicted: List or array of predicted values.

    Returns:
    - mse: Mean Squared Error.
    """
    if len(x_1) != len(x_2):
        raise ValueError("Input arrays must have the same length.")

    n = len(x_1)
    mse = sum((x_1[i] - x_2[i]) ** 2 for i in range(n)) / n

    return mse


def calculate_moments(data: np.ndarray) -> Tuple[float, float, float, float]:
    """
    Calculate moments (mean, variance, skewness, kurtosis) of a given vector.

    Parameters:
    - data: List or array of numerical data.

    Returns:
    - mean: Mean of the data.
    - variance: Variance of the data.
    - skewness: Skewness of the data.
    - kurt: Kurtosis of the data.
    """
    mean_val = np.mean(data)
    variance_val = np.var(data)
    skewness_val = skew(data)
    kurtosis_val = kurtosis(data)

    moments = {
        "Mean": mean_val,
        "Variance": variance_val,
        "Skewness": skewness_val,
        "Kurtosis": kurtosis_val,
    }

    pprint(moments)

    return mean_val, variance_val, skewness_val, kurtosis_val


def conditional_expectation(
    data: pd.Series,
    model: pd.Series,
    starting_point: float,
    target_level: float,
    T: int,
) -> float:
    """
    Compute numerically the conditional expectation of the spread reaching a certain level
    in a given amount of time T from a chosen starting point.

    Parameters:
    data (pd.Series): Real data containing the spread values.
    model (pd.Series): Model fit containing the predicted spread values.
    starting_point (float): Starting point for the spread.
    target_level (float): The level to be reached.
    T (int): Number of periods.

    Returns:
    float: Conditional expectation of the spread reaching the target level in T periods.
    """

    simulated_spread = model[:T]
    conditional_expectation = np.mean(simulated_spread >= target_level)

    return conditional_expectation


def expected_time_to_target(
    data: pd.Series,
    model: pd.Series,
    starting_point: float,
    target_level: float,
    max_periods: int,
) -> int:
    """
    Compute numerically the expected time (number of periods) it takes for the process to
    hit a certain level from a given starting point.

    Parameters:
    data (pd.Series): Real data containing the spread values.
    model (pd.Series): Model fit containing the predicted spread values.
    starting_point (float): Starting point for the spread.
    target_level (float): The level to be reached.
    max_periods (int): Maximum number of periods to simulate.

    Returns:
    int: Expected time (number of periods) to hit the target level.
    """

    time_to_target = np.argmax(model >= target_level)

    return time_to_target
