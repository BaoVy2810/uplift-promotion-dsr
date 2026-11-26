import numpy as np
import pandas as pd
from uplift_lab.data import normalize_group_name, split_data_stratified
from uplift_lab.evaluate import calculate_mean_and_ci, calculate_ate, calculate_smd
from uplift_lab.profit import calculate_expected_incremental_profit, rank_customers_by_policy


def test_normalize_group_name():
    assert normalize_group_name("Mens E-Mail") == "men"
    assert normalize_group_name("Womens E-Mail") == "women"
    assert normalize_group_name("No E-Mail") == "control"


def test_calculate_mean_and_ci():
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    res = calculate_mean_and_ci(s)
    assert res["n"] == 5.0
    assert np.isclose(res["mean"], 3.0)
    assert res["ci_low"] < 3.0 < res["ci_high"]


def test_calculate_ate():
    y1 = pd.Series([1, 1, 1, 0, 1])
    y0 = pd.Series([0, 0, 1, 0, 0])
    res = calculate_ate(y1, y0)
    assert np.isclose(res["ate"], 0.6)
    assert res["ci_low"] < 0.6 < res["ci_high"]
    assert res["p_value"] < 0.1


def test_profit_model():
    tau = np.array([0.10, 0.01, -0.05])
    p_t = np.array([0.20, 0.80, 0.10])
    margin = 10.0
    delta = 1.0
    c = 0.05

    # Customer 0: 0.10*10 - 1.0*0.20 - 0.05 = 1.0 - 0.20 - 0.05 = 0.75 > 0
    # Customer 1 (Sure Thing): 0.01*10 - 1.0*0.80 - 0.05 = 0.10 - 0.80 - 0.05 = -0.75 < 0
    # Customer 2 (Sleeping Dog): -0.05*10 - 1.0*0.10 - 0.05 = -0.50 - 0.10 - 0.05 = -0.65 < 0
    profits = calculate_expected_incremental_profit(tau, p_t, margin, delta, c)
    assert np.isclose(profits[0], 0.75)
    assert np.isclose(profits[1], -0.75)
    assert np.isclose(profits[2], -0.65)

    ranking_profit = rank_customers_by_policy("profit_uplift", tau, p_t, margin, delta, c)
    assert ranking_profit[0] == 0  # Customer 0 is best
    assert ranking_profit[2] == 1  # Customer 1 is worst (Sure Thing penalized by high delta*p_t)
