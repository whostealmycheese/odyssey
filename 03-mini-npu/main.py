"""
Mini NPU Simulator: Main Entry Point
콘솔 애플리케이션 진입점 및 모드 선택, 키보드 인터럽트(Ctrl+C) 예외 방어 인터페이스입니다.
"""

import sys
from pathlib import Path

from mode1_user_input import run_mode1
from mode2_analysis import run_mode2
from benchmark import run_benchmark
from bonus_features import run_optimization_benchmark, generate_pattern


def print_main_banner() -> None:
    """메인 배너 출력"""
    print("\n" + "=" * 48)
    print("      🧠 Mini NPU MAC 연산 시뮬레이터 🧠")
    print("=" * 48)
    print("  1. 사용자 직접 입력 (3x3 필터 및 패턴 분석)")
    print("  2. data.json 데이터셋 일괄 분석 및 판정")
    print("  3. 크기별(3x3~25x25) O(N²) 성능 벤치마크")
    print("  4. [보너스] 1차원 평탄화 메모리 최적화 비교")
    print("  5. 프로그램 종료")
    print("=" * 48)


def get_menu_choice() -> int:
    """공통 메뉴 입력 처리 및 예외 방어"""
    while True:
        try:
            raw = input("모드를 선택하세요 (1-5): ").strip()
            if not raw:
                print("⚠️ [입력 오류] 번호를 입력해 주세요.\n")
                continue
            val = int(raw)
            if 1 <= val <= 5:
                return val
            print("⚠️ [범위 초과] 1부터 5 사이의 숫자를 입력해 주세요.\n")
        except ValueError:
            print("⚠️ [형식 오류] 숫자로만 입력해 주세요. (예: 1, 2)\n")


def main() -> None:
    """메인 실행 루프"""
    data_file = Path(__file__).resolve().parent / "data.json"

    try:
        while True:
            print_main_banner()
            choice = get_menu_choice()

            if choice == 1:
                run_mode1()
            elif choice == 2:
                run_mode2(data_file)
                # 과제 요구사항: data.json 분석 모드 수행 후 크기별 성능 분석 및 요약 출력
                print("\n[data.json 분석 모드 연계 크기별 성능 벤치마크]")
                run_benchmark(sizes=[3, 5, 13, 25], iterations=10)
            elif choice == 3:
                run_benchmark(sizes=[3, 5, 13, 25], iterations=10)
            elif choice == 4:
                run_optimization_benchmark(size=25, iterations=100)
            elif choice == 5:
                print("\n👋 Mini NPU 시뮬레이터를 종료합니다. 감사합니다!\n")
                sys.exit(0)

            input("\n[Enter] 키를 누르면 메인 메뉴로 돌아갑니다...")

    except KeyboardInterrupt:
        print("\n\n⚠️ [종료 감지] 사용자에 의해 Ctrl+C 신호가 입력되었습니다.")
        print("👋 안전하게 프로그램을 종료합니다. 안녕히 가세요!\n")
        sys.exit(0)
    except EOFError:
        print("\n\n👋 입력 스트림이 종료되어 안전하게 프로그램을 종료합니다.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
