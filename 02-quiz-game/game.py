"""
QuizGame Controller Module
게임의 전반적인 라이프사이클(메뉴 표시, 입력 유효성 검증, 화면 출력)을 관리합니다.
"""

import json
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

    def load_state(self) -> None:
        """
        state.json 파일에서 퀴즈 목록과 최고 점수를 불러옴
        - 파일 부재 시 기본 퀴즈 데이터로 자동 생성
        - 파일 손상(JSONDecodeError) 시 안전하게 기본값 복구
        """
        if not self.state_file.exists():
            print("📂 저장된 데이터 파일이 없어 기본 퀴즈 데이터셋을 초기화합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = 0
            self.save_state()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            raw_quizzes = data.get("quizzes", [])
            self.quizzes = [Quiz.from_dict(item) for item in raw_quizzes]
            self.best_score = int(data.get("best_score", 0))

            # 퀴즈 목록이 비어있는 비정상 상태 방어
            if not self.quizzes:
                print("⚠️ [경고] 퀴즈 목록이 비어있어 기본 퀴즈 데이터를 복원합니다.")
                self.quizzes = get_default_quizzes()
                self.save_state()

            # 카테고리 목록 동적 갱신
            for q in self.quizzes:
                if q.category not in self.categories:
                    self.categories.append(q.category)

            print(f"📂 [데이터 로드 성공] 총 {len(self.quizzes)}문항, 역대 최고 점수: {self.best_score}점")

        except (json.JSONDecodeError, UnicodeDecodeError, KeyError, ValueError) as e:
            print(f"⚠️ [데이터 손상 감지] {self.state_file.name} 파일 손상 오류: {e}")
            print("🔄 기본 퀴즈 데이터로 복구 후 새로 저장합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = 0
            self.save_state()
        except OSError as e:
            print(f"❌ [파일 읽기 실패] I/O 오류 발생: {e}")
            self.quizzes = get_default_quizzes()
            self.best_score = 0

    def save_state(self) -> bool:
        """
        현재 퀴즈 목록과 최고 점수를 state.json 파일에 UTF-8 인코딩으로 저장
        """
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score
        }
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except OSError as e:
            print(f"❌ [파일 저장 오류] 데이터를 파일에 기록하지 못했습니다: {e}")
            return False

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
