"""
Mode 2: data.json Batch Analysis Module
data.json에 저장된 필터와 패턴을 로드하여 크기별 일괄 MAC 연산 및 판정,
PASS/FAIL 판별 및 실패 케이스 요약 리포트를 생성합니다.
"""

from pathlib import Path
from typing import Dict, Any, List
from mac_engine import compute_mac, compare_scores
from data_loader import load_and_normalize_data, extract_size_from_key, validate_matrix_shape


def run_mode2(data_path: Path) -> Dict[str, Any]:
    """
    모드 2: data.json 일괄 분석 파이프라인
    :param data_path: data.json 경로
    :return: 분석 요약 통계 딕셔너리
    """
    print("\n" + "=" * 44)
    print("  모드 2: data.json 데이터셋 일괄 분석")
    print("=" * 44)

    # 1. 필터 및 패턴 로드
    data = load_and_normalize_data(data_path)
    filters = data["filters"]
    patterns = data["patterns"]

    print("\n#---------------------------------------")
    print("# [1] 필터 로드")
    print("#---------------------------------------")
    for size_key in sorted(filters.keys(), key=lambda k: int(k.split("_")[1])):
        labels = list(filters[size_key].keys())
        print(f"✓ {size_key} 필터 로드 완료 ({', '.join(labels)})")

    # 2. 패턴 분석
    print("\n#---------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 및 Epsilon 정책 적용)")
    print("#---------------------------------------")

    total_tests = len(patterns)
    passed_count = 0
    failed_cases: List[Dict[str, str]] = []

    for p_key, p_val in patterns.items():
        print(f"\n--- {p_key} ---")
        pattern_mat = p_val["input"]
        expected = p_val["expected"]
        raw_expected = p_val["raw_expected"]

        # 2-1. 크기 추출 및 해당 필터 조회
        try:
            size_n = extract_size_from_key(p_key)
            size_key = f"size_{size_n}"
        except ValueError as e:
            print(f"❌ [키 오류] {e} | FAIL")
            failed_cases.append({"case": p_key, "reason": str(e)})
            continue

        if size_key not in filters:
            msg = f"해당 크기 필터 부재 ({size_key})"
            print(f"❌ [필터 오류] {msg} | FAIL")
            failed_cases.append({"case": p_key, "reason": msg})
            continue

        flt_cross = filters[size_key].get("Cross")
        flt_x = filters[size_key].get("X")

        # 2-2. 패턴 행렬 유효성 및 크기 일치 검증 (비정상 종료 방어)
        is_valid_p, p_err = validate_matrix_shape(pattern_mat, size_n)
        if not is_valid_p:
            msg = f"패턴 형상 불일치: {p_err}"
            print(f"❌ [형상 오류] {msg} | FAIL")
            failed_cases.append({"case": p_key, "reason": msg})
            continue

        is_valid_f, f_err = validate_matrix_shape(flt_cross, size_n)
        if not is_valid_f:
            msg = f"필터 형상 불일치: {f_err}"
            print(f"❌ [형상 오류] {msg} | FAIL")
            failed_cases.append({"case": p_key, "reason": msg})
            continue

        # 2-3. MAC 점수 계산
        score_cross = compute_mac(pattern_mat, flt_cross)
        score_x = compute_mac(pattern_mat, flt_x)

        # 2-4. 허용오차(1e-9) 기반 판정
        decision, is_tie = compare_scores(score_cross, score_x, label_a="Cross", label_b="X", epsilon=1e-9)

        print(f"Cross 점수: {score_cross:.16f}")
        print(f"X 점수    : {score_x:.16f}")

        # 2-5. Expected와 일치 여부 판별
        if decision == expected:
            print(f"판정: {decision} | expected: {expected} ('{raw_expected}') | PASS")
            passed_count += 1
        else:
            if is_tie:
                fail_reason = "동점(UNDECIDED) 처리 규칙에 따라 FAIL (부동소수점 허용오차 |Cross-X| < 1e-9)"
            else:
                fail_reason = f"예측({decision})과 expected({expected}) 불일치"

            print(f"판정: {decision} | expected: {expected} ('{raw_expected}') | FAIL ({fail_reason})")
            failed_cases.append({"case": p_key, "reason": fail_reason})

    # 3. 결과 요약
    failed_count = len(failed_cases)
    print("\n#---------------------------------------")
    print("# [3] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트 : {total_tests}개")
    print(f"통과 (PASS): {passed_count}개")
    print(f"실패 (FAIL): {failed_count}개")

    if failed_cases:
        print("\n실패 케이스 목록:")
        for fc in failed_cases:
            print(f"  - {fc['case']}: {fc['reason']}")
    else:
        print("\n모든 케이스가 성공적으로 PASS 되었습니다!")
    print("=" * 44)

    return {
        "total": total_tests,
        "passed": passed_count,
        "failed": failed_count,
        "failed_cases": failed_cases
    }
