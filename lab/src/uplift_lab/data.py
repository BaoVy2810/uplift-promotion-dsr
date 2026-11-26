"""
Mô-đun quản lý, nạp và phân chia dữ liệu thử nghiệm ngẫu nhiên có đối chứng (RCT).
"""

from pathlib import Path
from typing import Dict, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklift.datasets import fetch_hillstrom


def normalize_group_name(segment_name: str) -> str:
    """Chuẩn hóa tên nhóm can thiệp Hillstrom sang mã nhị phân gọn gàng.

    Args:
        segment_name: Chuỗi gốc trong cột segment ('Mens E-Mail', 'Womens E-Mail', 'No E-Mail')

    Returns:
        'women' | 'men' | 'control'
    """
    s = str(segment_name).lower()
    if "women" in s:
        return "women"
    if "men" in s:
        return "men"
    return "control"


def load_hillstrom_data(
    data_home: Optional[Path] = None,
) -> pd.DataFrame:
    """Nạp dữ liệu thử nghiệm Hillstrom MineThatData đầy đủ cả 3 biến kết quả.

    Ghép các biến kết quả (visit, conversion, spend) vào cùng một DataFrame duy nhất.

    Args:
        data_home: Đường dẫn lưu dữ liệu gốc. Nếu None, mặc định là data/raw.

    Returns:
        DataFrame chứa 64.000 dòng với 8 đặc trưng và 3 biến kết quả.
    """
    target_cols = ["visit", "conversion", "spend"]
    bunches = {}
    path_str = str(data_home) if data_home else None

    for col in target_cols:
        bunches[col] = fetch_hillstrom(target_col=col, data_home=path_str)

    base = bunches["visit"]
    df = base.data.copy()
    df["segment"] = base.treatment.astype(str).values
    df["group"] = df["segment"].map(normalize_group_name)

    for col in target_cols:
        df[col] = bunches[col].target.values

    return df


def split_data_stratified(
    df: pd.DataFrame,
    treatment_col: str = "treatment",
    outcome_col: str = "visit",
    train_size: float = 0.60,
    val_size: float = 0.20,
    test_size: float = 0.20,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Phân chia tập dữ liệu train/validation/test phân tầng 2 chiều (stratified).

    Bảo đảm phân phối của cả biến can thiệp (treatment) và biến kết quả (outcome)
    đồng nhất trên cả 3 tập con theo đúng quy chuẩn Pre-Analysis Plan.

    Args:
        df: DataFrame đầu vào
        treatment_col: Tên cột chỉ định can thiệp (0/1)
        outcome_col: Tên cột chỉ định kết quả chuyển đổi (0/1)
        train_size: Tỷ lệ tập huấn luyện (mặc định 0.60)
        val_size: Tỷ lệ tập thẩm định (mặc định 0.20)
        test_size: Tỷ lệ tập kiểm định (mặc định 0.20)
        random_state: Hạt giống ngẫu nhiên cố định (mặc định 42)

    Returns:
        Tuple[train_df, val_df, test_df]
    """
    assert np.isclose(train_size + val_size + test_size, 1.0), "Tổng các tỷ lệ chia phải bằng 1.0"

    # Tạo khóa phân tầng kết hợp: ví dụ T=1_Y=0
    strat_key = df[treatment_col].astype(str) + "_" + df[outcome_col].astype(str)

    # Bước 1: Tách tập train
    train_df, temp_df = train_test_split(
        df,
        train_size=train_size,
        stratify=strat_key,
        random_state=random_state,
    )

    # Bước 2: Tách validation và test từ phần còn lại
    relative_val_size = val_size / (val_size + test_size)
    temp_strat_key = temp_df[treatment_col].astype(str) + "_" + temp_df[outcome_col].astype(str)

    val_df, test_df = train_test_split(
        temp_df,
        train_size=relative_val_size,
        stratify=temp_strat_key,
        random_state=random_state,
    )

    return (
        train_df.reset_index(drop=True),
        val_df.reset_index(drop=True),
        test_df.reset_index(drop=True),
    )
