"""
Mode 1: User Direct Input Module (3x3)
사용자가 직접 3x3 필터 2개(A, B)와 패턴을 콘솔로 입력하고,
입력 유효성 검증, MAC 점수 계산 및 연산 시간, 판정 결과를 출력합니다.
"""

import time
from typing import List
from mac_engine import compute_mac, compare_scores


def input_matrix_3x3(title: str) -> List[List[float]]:
    """
    3줄(줄당 3개 공백 구분 숫자) 입력을 안전하게 받아 3x3 행렬로 반환
    행/열 불일치, 파싱 오류 시 안내 메시지 출력 후 재입력 유도
    """
    print(f"\n{title} (3줄 입력, 공백 구분):")
    matrix: List[List[float]] = []

    r = 1
    while r <= 3:
        try:
            line = input(f"  {r}행 입력: ").strip()
            if not line:
                print("  ⚠️ [입력 오류] 빈 줄입니다. 3개의 숫자를 공백으로 구분하여 입력하세요.")
                continue

            tokens = line.split()
            if len(tokens) != 3:
                print(f"  ⚠️ [입력 형식 오류] 각 줄에 정확히 3개의 숫자를 공백으로 구분해 입력하세요. (현재: {len(tokens)}개)")
                continue

            row_floats = [float(x) for x in tokens]
            matrix.append(row_floats)
            r += 1
        except ValueError:
            print("  ⚠️ [숫자 파싱 오류] 올바른 숫자를 입력하세요. (예: 0 1 0)")

    return matrix


def run_mode1() -> None:
    """모드 1 메인 실행 파이프라인"""
    print("\n" + "=" * 44)
    print("  모드 1: 사용자 입력 (3x3 NPU 시뮬레이션)")
    print("=" * 44)

    # 1. 필터 A, B 입력
    print("\n#---------------------------------------")
    print("# [1] 필터 입력")
    print("#---------------------------------------")
    filter_a = input_matrix_3x3("필터 A")
    filter_b = input_matrix_3x3("필터 B")

    # 2. 패턴 입력
    print("\n#---------------------------------------")
    print("# [2] 패턴 입력")
    print("#---------------------------------------")
    pattern = input_matrix_3x3("입력 패턴")

    # 3. MAC 연산 및 10회 반복 순수 연산 시간 측정
    print("\n#---------------------------------------")
    print("# [3] MAC 결과")
    print("#---------------------------------------")

    # 순수 연산 10회 벤치마크
    times = []
    for _ in range(10):
        t0 = time.perf_counter()
        score_a = compute_mac(pattern, filter_a)
        score_b = compute_mac(pattern, filter_b)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000.0)  # ms 단위

    avg_time_ms = sum(times) / len(times)

    # 점수 판정
    decision, is_tie = compare_scores(score_a, score_b, label_a="A", label_b="B", epsilon=1e-9)

    print(f"A 점수: {score_a:.6f}")
    print(f"B 점수: {score_b:.6f}")
    print(f"연산 시간(평균/10회): {avg_time_ms:.4f} ms")

    if is_tie:
        print(f"판정: 판정 불가 (|A-B| < 1e-9 동점 규칙)")
    else:
        print(f"판정: {decision}")
    print("=" * 44)
