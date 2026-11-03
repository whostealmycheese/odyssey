"""
Data Loader & Schema Validation Module
data.json 로드, 키 규칙 파싱, 라벨 표준화(정규화) 및 배열 크기 유효성 검증을 담당합니다.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List


def normalize_label(raw_label: str) -> str:
    """
    다양한 형태의 라벨 입력을 표준 내부 라벨('Cross' 또는 'X')로 정규화합니다.
    - '+' 또는 'cross' -> 'Cross'
    - 'x' 또는 'X'     -> 'X'
    :param raw_label: 정규화 대상 문자열
    :return: 'Cross', 'X', 또는 'UNKNOWN'
    """
    cleaned = str(raw_label).strip().lower()
    if cleaned in ("+", "cross"):
        return "Cross"
    elif cleaned in ("x", "times"):
        return "X"
    return "UNKNOWN"


def extract_size_from_key(pattern_key: str) -> int:
    """
    'size_{N}_{idx}' 형식의 키에서 패턴 크기 N을 추출합니다.
    예: 'size_5_1' -> 5, 'size_13_2' -> 13
    """
    parts = pattern_key.split("_")
    if len(parts) >= 2 and parts[0] == "size":
        return int(parts[1])
    raise ValueError(f"지원하지 않는 키 형식입니다: {pattern_key} ('size_N_idx' 형식이어야 함)")


def validate_matrix_shape(mat: Any, expected_size: int) -> Tuple[bool, Optional[str]]:
    """
    2차원 배열의 행과 열 크기가 N x N과 정확히 일치하는지 검증합니다.
    """
    if not isinstance(mat, list) or len(mat) != expected_size:
        return False, f"행 수 불일치 (기대: {expected_size}, 실제: {len(mat) if isinstance(mat, list) else '비배열'})"

    for r_idx, row in enumerate(mat):
        if not isinstance(row, list) or len(row) != expected_size:
            return False, f"{r_idx}행의 열 수 불일치 (기대: {expected_size}, 실제: {len(row) if isinstance(row, list) else '비배열'})"

    return True, None


def load_and_normalize_data(json_path: Path) -> Dict[str, Any]:
    """
    data.json 파일을 읽어와 필터 라벨을 정규화하고 구조화된 딕셔너리로 반환합니다.
    :param json_path: data.json 경로
    :return: 정규화된 filters와 patterns 딕셔너리
    """
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    raw_filters = raw_data.get("filters", {})
    raw_patterns = raw_data.get("patterns", {})

    normalized_filters = {}
    for size_key, filter_pair in raw_filters.items():
        # filter_pair: {"cross": [...], "x": [...]}
        norm_pair = {}
        for k, v in filter_pair.items():
            norm_label = normalize_label(k)
            norm_pair[norm_label] = v
        normalized_filters[size_key] = norm_pair

    normalized_patterns = {}
    for p_key, p_val in raw_patterns.items():
        norm_expected = normalize_label(p_val.get("expected", ""))
        normalized_patterns[p_key] = {
            "input": p_val.get("input", []),
            "expected": norm_expected,
            "raw_expected": p_val.get("expected", "")
        }

    return {
        "filters": normalized_filters,
        "patterns": normalized_patterns
    }
