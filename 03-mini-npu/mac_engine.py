"""
MAC Engine Module
순수 파이썬 반복문을 사용한 2차원 MAC(Multiply-Accumulate) 연산 및
부동소수점 허용오차(Epsilon) 기반 비교 판정 엔진입니다.
"""

from typing import List, Tuple


def compute_mac(pattern: List[List[float]], filter_mat: List[List[float]]) -> float:
    """
    외부 라이브러리(NumPy 등) 없이 2차원 순수 반복문으로 MAC 연산을 수행합니다.
    MAC = Sum(Pattern[i][j] * Filter[i][j])
    :param pattern: N x N 입력 패턴 2차원 배열
    :param filter_mat: N x N 필터 2차원 배열
    :return: 곱셈-누적 결과 점수 (float)
    """
    if len(pattern) != len(filter_mat) or len(pattern[0]) != len(filter_mat[0]):
        raise ValueError(
            f"크기 불일치: 패턴 크기({len(pattern)}x{len(pattern[0])})와 "
            f"필터 크기({len(filter_mat)}x{len(filter_mat[0])})가 다릅니다."
        )

    score = 0.0
    rows = len(pattern)
    cols = len(pattern[0])

    for r in range(rows):
        for c in range(cols):
            score += float(pattern[r][c]) * float(filter_mat[r][c])

    return score


def compare_scores(
    score_a: float,
    score_b: float,
    label_a: str = "Cross",
    label_b: str = "X",
    epsilon: float = 1e-9
) -> Tuple[str, bool]:
    """
    부동소수점 오차를 고려한 허용오차(Epsilon) 기반 점수 비교 정책
    :param score_a: A(Cross) 필터 MAC 점수
    :param score_b: B(X) 필터 MAC 점수
    :param label_a: A 필터 식별자 라벨 (기본값: 'Cross')
    :param label_b: B 필터 식별자 라벨 (기본값: 'X')
    :param epsilon: 부동소수점 동점 판정 허용오차 (기본값: 1e-9)
    :return: (판정 결과 라벨, 동점 여부 bool)
    """
    diff = abs(score_a - score_b)

    # 허용오차 이내의 미세한 차이는 부동소수점 오차에 따른 동점으로 간주
    if diff < epsilon:
        return "UNDECIDED", True
    elif score_a > score_b:
        return label_a, False
    else:
        return label_b, False
