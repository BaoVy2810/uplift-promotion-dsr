"""
Mô-đun mô hình hóa lợi nhuận kinh tế (Profit Model) và đánh giá chi phí
cho các chính sách nhắm mục tiêu khuyến mãi.

Dựa trên khung lý thuyết của Haupt & Lessmann (2022) và Verbeke et al. (2023).
"""

from typing import Dict, List, Optional
import numpy as np
import pandas as pd


def calculate_expected_incremental_profit(
    tau: np.ndarray,
    p_treatment: np.ndarray,
    margin: float,
    discount_cost: float,
    contact_cost: float,
) -> np.ndarray:
    """Tính lợi nhuận gia tăng kỳ vọng của từng khách hàng: Delta_Pi(i).

    Công thức:
        Delta_Pi(i) = tau(i) * m - delta * p_T(i) - c

    Trong đó:
        - tau(i): Điểm uplift ước lượng = p_T(i) - p_C(i)
        - p_treatment: Xác suất mua khi nhận khuyến mãi p_T(i)
        - margin (m): Biên lợi nhuận gộp trên một đơn hàng (chưa trừ khuyến mãi)
        - discount_cost (delta): Chi phí ưu đãi/chiết khấu thực tế trên mỗi đơn dùng mã
        - contact_cost (c): Chi phí tiếp cận/gửi thông điệp cố định trên mỗi khách hàng

    Args:
        tau: Mảng uplift ước lượng
        p_treatment: Mảng xác suất mua dưới can thiệp
        margin: Biên lợi nhuận m
        discount_cost: Chi phí ưu đãi delta
        contact_cost: Chi phí tiếp cận c

    Returns:
        Mảng lợi nhuận gia tăng kỳ vọng cho từng khách hàng
    """
    return tau * margin - discount_cost * p_treatment - contact_cost


def rank_customers_by_policy(
    policy: str,
    tau: np.ndarray,
    p_treatment: np.ndarray,
    margin: float = 10.0,
    discount_cost: float = 2.0,
    contact_cost: float = 0.05,
    random_seed: int = 42,
) -> np.ndarray:
    """Xếp hạng thứ tự ưu tiên của khách hàng theo 4 chính sách nhắm mục tiêu.

    Các chính sách:
        1. 'random': Xếp hạng ngẫu nhiên
        2. 'propensity': Xếp theo xác suất mua p_T(i) giảm dần (dễ sa vào Sure Things)
        3. 'uplift': Xếp theo điểm uplift tau(i) giảm dần (tập trung Persuadables)
        4. 'profit_uplift': Xếp theo lợi nhuận gia tăng kỳ vọng Delta_Pi(i) giảm dần

    Args:
        policy: Tên chính sách ('random' | 'propensity' | 'uplift' | 'profit_uplift')
        tau: Mảng điểm uplift
        p_treatment: Mảng xác suất mua p_T
        margin: Biên lợi nhuận
        discount_cost: Chi phí ưu đãi delta
        contact_cost: Chi phí tiếp cận c
        random_seed: Hạt giống ngẫu nhiên

    Returns:
        Mảng các chỉ số (indices) đã được sắp xếp giảm dần theo mức độ ưu tiên
    """
    n = len(tau)
    if policy == "random":
        rng = np.random.default_rng(random_seed)
        return rng.permutation(n)
    elif policy == "propensity":
        return np.argsort(-p_treatment)
    elif policy == "uplift":
        return np.argsort(-tau)
    elif policy == "profit_uplift":
        profit = calculate_expected_incremental_profit(
            tau=tau,
            p_treatment=p_treatment,
            margin=margin,
            discount_cost=discount_cost,
            contact_cost=contact_cost,
        )
        return np.argsort(-profit)
    else:
        raise ValueError(f"Chính sách '{policy}' không hợp lệ. Chọn: random, propensity, uplift, profit_uplift.")


def run_cost_sensitivity_grid(
    tau: np.ndarray,
    p_treatment: np.ndarray,
    margin: float,
    contact_costs: List[float],
    discount_costs: List[float],
) -> pd.DataFrame:
    """Chạy phân tích độ nhạy lợi nhuận trên một lưới tham số chi phí (c, delta).

    Args:
        tau: Mảng uplift
        p_treatment: Mảng xác suất mua
        margin: Biên lợi nhuận cơ sở
        contact_costs: Danh sách các mức chi phí tiếp cận c
        discount_costs: Danh sách các mức chi phí ưu đãi delta

    Returns:
        DataFrame tóm tắt tỷ lệ khách hàng có Delta_Pi > 0 và tổng lợi nhuận kỳ vọng.
    """
    rows = []
    n = len(tau)
    for c in contact_costs:
        for delta in discount_costs:
            profit = calculate_expected_incremental_profit(
                tau=tau,
                p_treatment=p_treatment,
                margin=margin,
                discount_cost=delta,
                contact_cost=c,
            )
            profitable_mask = profit > 0
            rows.append({
                "contact_cost_c": c,
                "discount_cost_delta": delta,
                "margin_m": margin,
                "profitable_customers_count": int(profitable_mask.sum()),
                "profitable_share": float(profitable_mask.mean()),
                "max_profit": float(profit[profitable_mask].sum()) if profitable_mask.any() else 0.0,
            })
    return pd.DataFrame(rows)
