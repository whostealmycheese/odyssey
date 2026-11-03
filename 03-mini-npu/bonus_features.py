"""
Bonus Features Module
1. N x N 크기의 십자가(Cross) 및 X 패턴 자동 생성기
2. 2차원 중첩 리스트 대비 1차원 평탄화(Flattened) 메모리 접근 최적화 벤치마크
"""

import time
from typing import List, Tuple
from mac_engine import compute_mac


def generate_pattern(size: int, pattern_type: str = "Cross") -> List[List[float]]:
    """
    임의의 크기 N에 대해 완벽한 대칭을 이루는 Cross(+) 또는 X 패턴 2차원 배열 생성
    :param size: N (홀수 권장, 예: 3, 5, 13, 25)
    :param pattern_type: 'Cross' 또는 'X'
    :return: N x N 2차원 패턴 리스트
    """
    matrix = [[0.0 for _ in range(size)] for _ in range(size)]
    mid = size // 2

    p_type = pattern_type.strip().lower()

    if p_type in ("cross", "+"):
        for r in range(size):
            matrix[r][mid] = 1.0
        for c in range(size):
            matrix[mid][c] = 1.0
    elif p_type in ("x", "times"):
        for r in range(size):
            matrix[r][r] = 1.0
            matrix[r][size - 1 - r] = 1.0
    else:
        raise ValueError(f"지원하지 않는 패턴 타입입니다: {pattern_type}")

    return matrix


def flatten_2d_to_1d(mat: List[List[float]]) -> List[float]:
    """2차원 행렬을 1차원 연속 메모리 배열(길이 N²)로 평탄화"""
    return [elem for row in mat for elem in row]


def compute_mac_1d(pattern_1d: List[float], filter_1d: List[float]) -> float:
    """1차원 평탄화 배열 대상 단일 루프 MAC 연산 (메모리 접근 오버헤드 감소)"""
    score = 0.0
    length = len(pattern_1d)
    for i in range(length):
        score += pattern_1d[i] * filter_1d[i]
    return score


def run_optimization_benchmark(size: int = 25, iterations: int = 100) -> Tuple[float, float, float]:
    """
    2차원 접근 vs 1차원 평탄화 접근 최적화 성능 비교 (동일 입력, iterations회 반복)
    """
    print("\n#---------------------------------------")
    print(f"# [보너스] 1차원 메모리 접근 최적화 벤치마크 ({size}x{size}, {iterations}회 반복)")
    print("#---------------------------------------")

    # 데이터 준비
    mat_p = generate_pattern(size, "Cross")
    mat_f = generate_pattern(size, "Cross")

    vec_p = flatten_2d_to_1d(mat_p)
    vec_f = flatten_2d_to_1d(mat_f)

    # 1. 기존 2차원 연산 시간 측정
    t0 = time.perf_counter()
    for _ in range(iterations):
        _ = compute_mac(mat_p, mat_f)
    t1 = time.perf_counter()
    time_2d_ms = (t1 - t0) * 1000.0 / iterations

    # 2. 최적화된 1차원 연산 시간 측정
    t2 = time.perf_counter()
    for _ in range(iterations):
        _ = compute_mac_1d(vec_p, vec_f)
    t3 = time.perf_counter()
    time_1d_ms = (t3 - t2) * 1000.0 / iterations

    # 성능 개선율 계산
    speedup = ((time_2d_ms - time_1d_ms) / time_2d_ms) * 100.0

    print(f"기존 2차원 중첩 루프 평균 연산 시간: {time_2d_ms:.4f} ms")
    print(f"최적화 1차원 단일 루프 평균 연산 시간: {time_1d_ms:.4f} ms")
    print(f"💡 메모리 인덱싱 접근 최적화 속도 향상: {speedup:+.1f}%")
    print("=" * 58)

    return time_2d_ms, time_1d_ms, speedup
