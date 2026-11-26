"""
Mô-đun kiểm định thống kê, đánh giá cân bằng ngẫu nhiên hóa (balance checks)
và ước lượng hiệu ứng can thiệp trung bình (ATE).
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def calculate_smd(
    df: pd.DataFrame,
    group_col: str,
    treatment_group: str,
    control_group: str,
    feature_cols: List[str],
) -> pd.Series:
    """Tính toán chênh lệch trung bình chuẩn hóa (Standardized Mean Difference - SMD).

    Công thức: SMD = (mean_T - mean_C) / sqrt((var_T + var_C) / 2)
    Quy ước quốc tế: |SMD| < 0.1 được xem là cân bằng lý tưởng giữa hai nhóm.

    Args:
        df: DataFrame chứa dữ liệu
        group_col: Cột định danh nhóm
        treatment_group: Giá trị nhóm can thiệp
        control_group: Giá trị nhóm đối chứng
        feature_cols: Danh sách các cột đặc trưng cần tính

    Returns:
        Series chứa giá trị SMD cho từng đặc trưng
    """
    treat = df[df[group_col] == treatment_group][feature_cols]
    ctrl = df[df[group_col] == control_group][feature_cols]

    mean_diff = treat.mean() - ctrl.mean()
    pooled_var = (treat.var(ddof=1) + ctrl.var(ddof=1)) / 2.0
    smd = mean_diff / np.sqrt(pooled_var)
    return smd


def test_randomization_balance(
    df: pd.DataFrame,
    group_col: str,
    num_cols: List[str],
    cat_cols: List[str],
) -> pd.DataFrame:
    """Kiểm tra tính cân bằng ngẫu nhiên hóa trước can thiệp.

    Áp dụng kiểm định Chi-bình phương cho biến phân loại và kiểm định Kruskal-Wallis
    cho biến liên tục qua tất cả các nhóm can thiệp.

    Args:
        df: DataFrame chứa dữ liệu
        group_col: Tên cột nhóm can thiệp
        num_cols: Danh sách biến số liên tục
        cat_cols: Danh sách biến rời rạc/phân loại

    Returns:
        DataFrame tổng hợp tên biến, loại kiểm định, giá trị thống kê và p-value.
    """
    records = []
    groups = df[group_col].unique()

    # Biến phân loại: Chi-Square Test of Independence
    for col in cat_cols:
        contingency = pd.crosstab(df[col], df[group_col])
        stat, p, dof, _ = stats.chi2_contingency(contingency)
        records.append({
            "variable": col,
            "type": "categorical",
            "test": "Chi-Square",
            "stat": stat,
            "p_value": p,
        })

    # Biến liên tục: Kruskal-Wallis H-test
    for col in num_cols:
        group_samples = [df.loc[df[group_col] == g, col].dropna() for g in groups]
        stat, p = stats.kruskal(*group_samples)
        records.append({
            "variable": col,
            "type": "continuous",
            "test": "Kruskal-Wallis",
            "stat": stat,
            "p_value": p,
        })

    return pd.DataFrame(records)


def calculate_mean_and_ci(
    series: pd.Series,
    alpha: float = 0.05,
) -> Dict[str, float]:
    """Tính trung bình mẫu và khoảng tin cậy 95% (hoặc mức alpha tùy chọn).

    Args:
        series: Chuỗi giá trị số hoặc nhị phân
        alpha: Mức ý nghĩa thống kê (mặc định 0.05 tương ứng KTC 95%)

    Returns:
        Dict chứa n, mean, std, se, ci_low, ci_high
    """
    clean_s = series.dropna()
    n = len(clean_s)
    m = float(clean_s.mean())
    s = float(clean_s.std(ddof=1))
    se = s / np.sqrt(n) if n > 0 else 0.0

    z_crit = stats.norm.ppf(1.0 - alpha / 2.0)
    ci_low = m - z_crit * se
    ci_high = m + z_crit * se

    return {
        "n": float(n),
        "mean": m,
        "std": s,
        "se": se,
        "ci_low": ci_low,
        "ci_high": ci_high,
    }


def calculate_ate(
    y_treatment: pd.Series,
    y_control: pd.Series,
    alpha: float = 0.05,
) -> Dict[str, float]:
    """Ước lượng Hiệu ứng can thiệp trung bình (Average Treatment Effect - ATE).

    Sử dụng ước lượng sai số chuẩn không đồng nhất phương sai (Neyman Variance Estimator)
    và kiểm định giả thuyết Z-test hai phía cho H0: ATE = 0.

    Args:
        y_treatment: Chuỗi kết quả nhóm can thiệp
        y_control: Chuỗi kết quả nhóm đối chứng
        alpha: Mức ý nghĩa (mặc định 0.05)

    Returns:
        Dict chứa ATE, sai số chuẩn (se), KTC 95% (ci_low, ci_high) và p_value.
    """
    n1 = len(y_treatment)
    n0 = len(y_control)
    m1 = y_treatment.mean()
    m0 = y_control.mean()

    diff = float(m1 - m0)
    var1 = y_treatment.var(ddof=1)
    var0 = y_control.var(ddof=1)

    se = float(np.sqrt(var1 / n1 + var0 / n0))
    z_crit = stats.norm.ppf(1.0 - alpha / 2.0)

    ci_low = diff - z_crit * se
    ci_high = diff + z_crit * se

    z_stat = diff / se if se > 0 else 0.0
    p_value = float(2.0 * (1.0 - stats.norm.cdf(abs(z_stat))))

    return {
        "ate": diff,
        "se": se,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "p_value": p_value,
    }
