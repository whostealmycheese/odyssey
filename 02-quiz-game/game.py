"""
QuizGame Controller Module
게임의 전반적인 라이프사이클(메뉴 표시, 입력 유효성 검증, 화면 출력)을 관리합니다.
"""

import sys
from pathlib import Path
from typing import List, Optional
from quiz import Quiz
from default_data import get_default_quizzes


def get_valid_integer(prompt: str, min_val: int, max_val: int) -> int:
    """
    공통 숫자 입력 처리 및 예외 검증 함수
    - 앞뒤 공백 제거
    - 빈 문자열 방어
    - 정수 변환 실패(문자 입력) 방어
    - 지정 범위 밖 입력 방어
    """
    while True:
        try:
            raw_input = input(prompt)
            cleaned = raw_input.strip()

            if not cleaned:
                print("⚠️ [입력 오류] 아무것도 입력되지 않았습니다. 번호를 입력해 주세요.\n")
                continue

            value = int(cleaned)
            if value < min_val or value > max_val:
                print(f"⚠️ [범위 초과] {min_val}부터 {max_val} 사이의 숫자를 입력해 주세요.\n")
                continue

            return value
        except ValueError:
            print("⚠️ [형식 오류] 숫자로만 입력해 주세요. (예: 1, 2, ...)\n")


def get_non_empty_string(prompt: str) -> str:
    """
    공백이 아닌 유효한 문자열 입력 처리 함수
    """
    while True:
        raw_input = input(prompt)
        cleaned = raw_input.strip()
        if not cleaned:
            print("⚠️ [입력 오류] 빈 내용은 입력할 수 없습니다. 내용을 작성해 주세요.\n")
            continue
        return cleaned


class QuizGame:
    """퀴즈 게임의 전체 흐름을 주관하는 핵심 컨트롤러 클래스"""

    def __init__(self, state_file: Optional[Path] = None):
        if state_file is None:
            self.state_file = Path(__file__).resolve().parent / "state.json"
        else:
            self.state_file = Path(state_file)

        self.quizzes: List[Quiz] = []
        self.best_score: int = 0
        self.categories: List[str] = ["개발/CS", "영화/문화", "일반상식"]

    def print_menu(self) -> int:
        """메인 메뉴 출력 및 사용자 선택 번호 반환"""
        print("\n" + "=" * 44)
        print("         🎯 나만의 멀티 주제 퀴즈 게임 🎯")
        print("=" * 44)
        print("  1. 퀴즈 풀기 (주제 선택 가능)")
        print("  2. 새로운 퀴즈 추가")
        print("  3. 등록된 퀴즈 목록 조회")
        print("  4. 최고 점수 확인")
        print("  5. 게임 종료")
        print("=" * 44)
        return get_valid_integer("메뉴 번호를 선택하세요 (1-5): ", 1, 5)
