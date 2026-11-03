"""
Main Application Entry Point
퀴즈 게임의 실행 진입점으로, 메인 이벤트 루프 및 KeyboardInterrupt(Ctrl+C) / EOFError
비정상 종료 방어 메커니즘을 총괄합니다.
"""

import sys
from game import QuizGame


def main() -> None:
    """퀴즈 게임 메인 실행 루프"""
    game = QuizGame()

    try:
        # 1. 초기 데이터 로드 (state.json 없을 시 기본값 자동 세팅)
        game.load_state()

        # 2. 메인 이벤트 루프
        while True:
            choice = game.print_menu()

            if choice == 1:
                game.play_quiz()
            elif choice == 2:
                game.add_quiz()
            elif choice == 3:
                game.list_quizzes()
            elif choice == 4:
                game.show_best_score()
            elif choice == 5:
                print("\n💾 현재 게임 상태를 안전하게 저장합니다...")
                game.save_state()
                print("👋 퀴즈 게임을 이용해 주셔서 감사합니다. 좋은 하루 되세요!\n")
                sys.exit(0)

    except KeyboardInterrupt:
        # 프로그램 실행 중 Ctrl+C 입력 시 비정상 종료 방어 및 안전 저장
        print("\n\n⚠️ [강제 종료 감지] 사용자에 의해 Ctrl+C 신호가 발생했습니다.")
        print("💾 현재 상태를 state.json에 안전하게 저장한 뒤 종료합니다.")
        game.save_state()
        print("👋 안전하게 종료되었습니다. 다음에 또 만나요!\n")
        sys.exit(0)

    except EOFError:
        # 입력 스트림 종료(EOF) 시 방어
        print("\n\n⚠️ [입력 종료 감지] 입력 스트림이 종료되었습니다.")
        game.save_state()
        print("👋 안전하게 종료되었습니다.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
