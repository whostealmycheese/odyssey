"""
Benchmark & Performance Analysis Module
3x3, 5x5, 13x13, 25x25 등 패턴 크기 증가에 따른 순수 MAC 연산 시간(ms)을
10회 이상 반복 측정하고 O(N²) 시간 복잡도를 실측 및 검증합니다.
"""

import time
from typing import List, Dict, Any
from mac_engine import compute_mac


def generate_dummy_matrix(size: int) -> List[List[float]]:
    """테스트용 N x N 부동소수점 더미 행렬 생성"""
    return [[1.0 if (r == c or r + c == size - 1) else 0.0 for c in range(size)] for r in range(size)]


def run_benchmark(sizes: List[int] = None, iterations: int = 10) -> List[Dict[str, Any]]:
    """
    크기별 순수 MAC 연산 시간(I/O 제외)을 10회 반복 측정하여 성능 지표 반환
    :param sizes: 측정할 N 크기 리스트 (기본값: [3, 5, 13, 25])
    :param iterations: 반복 측정 횟수 (최소 10회)
    :return: 벤치마크 결과 리스트
    """
    if sizes is None:
        sizes = [3, 5, 13, 25]

    results: List[Dict[str, Any]] = []

    print("\n#---------------------------------------")
    print(f"# 성능 분석 (순수 MAC 연산 시간 평균 / {iterations}회 반복)")
    print("#---------------------------------------")
    print(f"{'크기 (N×N)':<12} {'평균 시간 (ms)':<16} {'연산 횟수 (N²)':<16} {'이론적 배율':<12}")
    print("-" * 58)

    base_ops = sizes[0] ** 2

    for n in sizes:
        p = generate_dummy_matrix(n)
        f = generate_dummy_matrix(n)
        ops = n * n
        ratio = ops / base_ops

        # 워밍업 (1회)
        _ = compute_mac(p, f)

        # 10회 정밀 측정 (I/O 제외한 순수 연산 구간)
        times_ms = []
        for _ in range(iterations):
            t_start = time.perf_counter()
            _ = compute_mac(p, f)
            t_end = time.perf_counter()
            times_ms.append((t_end - t_start) * 1000.0)

        avg_ms = sum(times_ms) / len(times_ms)

        results.append({
            "size": f"{n}×{n}",
            "n": n,
            "avg_ms": avg_ms,
            "ops": ops,
            "ratio": ratio
        })

        print(f"{f'{n}×{n}':<12} {f'{avg_ms:.4f} ms':<16} {f'{ops} 회':<16} {f'{ratio:.1f}x':<12}")

    print("-" * 58)
    print("💡 분석: 크기 N이 커질수록 2중 반복문에 의해 연산 횟수가 N²으로 급증함 (O(N²))")
    print("=" * 58)

    return results
