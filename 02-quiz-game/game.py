"""
QuizGame Controller Module
게임의 전반적인 라이프사이클(메뉴 표시, 입력 유효성 검증, 화면 출력)을 관리합니다.
"""

import json
import random
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

    def list_quizzes(self) -> None:
        """등록된 전체 퀴즈 목록을 주제별로 보기 쉽게 출력"""
        print("\n" + "=" * 44)
        print("          📋 등록된 전체 퀴즈 목록")
        print("=" * 44)

        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 메뉴에서 새 퀴즈를 추가해 보세요.")
            return

        print(f"총 {len(self.quizzes)}개의 퀴즈가 등록되어 있습니다.\n")
        for idx, q in enumerate(self.quizzes, start=1):
            print(f"[{idx}] [{q.category}] {q.question}")
            for c_idx, choice in enumerate(q.choices, start=1):
                marker = " ★(정답)" if c_idx == q.answer else ""
                print(f"    {c_idx}. {choice}{marker}")
            print("-" * 44)

    def show_best_score(self) -> None:
        """역대 최고 점수 확인"""
        print("\n" + "=" * 44)
        print("          🏆 역대 최고 점수 명예의 전당")
        print("=" * 44)

        if self.best_score == 0:
            print("🎯 아직 기록된 최고 점수가 없습니다.")
            print("   메뉴 1번을 선택해 첫 번째 퀴즈에 도전해 보세요!")
        else:
            print(f"⭐ 현재 최고 점수: {self.best_score}점")
            print("   새로운 최고 기록을 경신하기 위해 계속 도전해 보세요!")
        print("=" * 44)

    def play_quiz(self) -> None:
        """주제 선택 및 퀴즈 출제, 실시간 채점, 최고 점수 갱신 루프"""
        print("\n" + "=" * 44)
        print("          📝 퀴즈 풀기 모드")
        print("=" * 44)

        if not self.quizzes:
            print("⚠️ 출제 가능한 퀴즈가 없습니다. 퀴즈를 먼저 등록해 주세요.")
            return

        # 1. 주제 선택 메뉴
        print("도전할 퀴즈 주제를 선택해 주세요:")
        for idx, cat in enumerate(self.categories, start=1):
            count = sum(1 for q in self.quizzes if q.category == cat)
            print(f"  {idx}. {cat} ({count}문제)")
        all_option_num = len(self.categories) + 1
        print(f"  {all_option_num}. 전체 주제 섞어서 풀기 (총 {len(self.quizzes)}문제)")

        choice = get_valid_integer("선택: ", 1, all_option_num)

        if choice <= len(self.categories):
            selected_cat = self.categories[choice - 1]
            target_quizzes = [q for q in self.quizzes if q.category == selected_cat]
        else:
            selected_cat = "전체 주제"
            target_quizzes = list(self.quizzes)

        if not target_quizzes:
            print(f"⚠️ [{selected_cat}] 주제에 등록된 문제가 없습니다.")
            return

        # 2. 문제 출제 준비 (랜덤 셔플)
        pool = list(target_quizzes)
        random.shuffle(pool)

        total_questions = len(pool)
        correct_count = 0

        print(f"\n🚀 [{selected_cat}] 퀴즈를 시작합니다! (총 {total_questions}문항)\n" + "-" * 44)

        # 3. 퀴즈 출제 및 풀이 루프
        for q_idx, quiz in enumerate(pool, start=1):
            quiz.display(q_idx)
            user_choice = get_valid_integer("정답 입력 (1-4): ", 1, 4)

            if quiz.is_correct(user_choice):
                print("✅ 정답입니다! (+10점)")
                correct_count += 1
            else:
                correct_answer_text = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다. (정답: {quiz.answer}번 - {correct_answer_text})")

            print("-" * 44)

        # 4. 점수 계산 및 결과 출력
        score = int((correct_count / total_questions) * 100)
        print("\n" + "=" * 44)
        print(f"🏆 최종 결과: {total_questions}문제 중 {correct_count}문제 정답! ({score}점)")

        # 5. 최고 점수 갱신 판별 및 영속화
        if score > self.best_score:
            print(f"🎉 와우! 새로운 역대 최고 점수를 달성했습니다! ({self.best_score}점 ➔ {score}점)")
            self.best_score = score
            self.save_state()
        else:
            print(f"현재 역대 최고 점수: {self.best_score}점")
        print("=" * 44)

    def add_quiz(self) -> None:
        """새로운 퀴즈를 입력받아 등록하고 state.json에 실시간 저장"""
        print("\n" + "=" * 44)
        print("          📌 새로운 퀴즈 추가")
        print("=" * 44)

        # 주제(카테고리) 선택 또는 직접 입력
        print("퀴즈 주제(카테고리)를 선택하세요:")
        for idx, cat in enumerate(self.categories, start=1):
            print(f"  {idx}. {cat}")
        print(f"  {len(self.categories) + 1}. 새로운 주제 직접 입력")

        cat_choice = get_valid_integer("선택: ", 1, len(self.categories) + 1)
        if cat_choice <= len(self.categories):
            selected_category = self.categories[cat_choice - 1]
        else:
            selected_category = get_non_empty_string("새로운 주제 이름을 입력하세요 (예: 과학, 역사): ")
            if selected_category not in self.categories:
                self.categories.append(selected_category)

        # 문제 및 4지선다 선택지 입력
        print(f"\n[{selected_category}] 주제의 퀴즈 정보를 입력합니다.")
        question = get_non_empty_string("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = get_non_empty_string(f"선택지 {i}: ")
            choices.append(choice)

        answer = get_valid_integer("정답 번호 (1-4): ", 1, 4)

        # 객체 생성 및 목록 추가
        new_quiz = Quiz(
            question=question,
            choices=choices,
            answer=answer,
            category=selected_category
        )
        self.quizzes.append(new_quiz)

        if self.save_state():
            print(f"\n✅ 퀴즈가 성공적으로 등록되고 파일에 저장되었습니다! (총 {len(self.quizzes)}문항)")
        else:
            print("\n⚠️ 퀴즈는 메모리에 추가되었으나 파일 저장에 실패했습니다.")

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
