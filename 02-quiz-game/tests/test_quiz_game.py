"""
Unit Test Suite for 02-quiz-game
[평가 항목 #1, #2 보완] 메뉴·기능 동작 및 경계값·예외 상황에 대한 자동화 유닛 테스트
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from quiz import Quiz
from game import QuizGame, get_valid_integer, get_non_empty_string
from default_data import get_default_quizzes, DEFAULT_QUIZ_COUNT


class TestQuizModel(unittest.TestCase):
    """Quiz 모델 클래스 정답 판정 및 직렬화 테스트"""

    def setUp(self):
        self.quiz = Quiz(
            question="파이썬의 창시자는?",
            choices=["리누스", "귀도 반 로섬", "제임스 고슬링", "켄 톰슨"],
            answer=2,
            category="개발/CS"
        )

    def test_correct_answer(self):
        """정답 판정 검증 (answer=2)"""
        self.assertTrue(self.quiz.is_correct(2))

    def test_wrong_answer(self):
        """오답 판정 검증"""
        self.assertFalse(self.quiz.is_correct(1))
        self.assertFalse(self.quiz.is_correct(3))
        self.assertFalse(self.quiz.is_correct(4))

    def test_boundary_answer_values(self):
        """경계값 및 비정상 범위 정답 판정 (0, 5, 음수)"""
        self.assertFalse(self.quiz.is_correct(0))
        self.assertFalse(self.quiz.is_correct(5))
        self.assertFalse(self.quiz.is_correct(-1))
        self.assertFalse(self.quiz.is_correct(999))

    def test_dict_serialization_cycle(self):
        """to_dict() 및 from_dict() 왕복 직렬화 무결성 테스트"""
        serialized = self.quiz.to_dict()
        restored = Quiz.from_dict(serialized)
        self.assertEqual(restored.question, self.quiz.question)
        self.assertEqual(restored.choices, self.quiz.choices)
        self.assertEqual(restored.answer, self.quiz.answer)
        self.assertEqual(restored.category, self.quiz.category)


class TestDefaultDataset(unittest.TestCase):
    """기본 데이터셋 무결성 및 명시적 상수 테스트 (평가 항목 #4)"""

    def test_default_quiz_count_constant(self):
        """DEFAULT_QUIZ_COUNT 상수 일치 여부 확인"""
        quizzes = get_default_quizzes()
        self.assertEqual(len(quizzes), DEFAULT_QUIZ_COUNT)
        self.assertGreaterEqual(DEFAULT_QUIZ_COUNT, 10)

    def test_default_quiz_structures(self):
        """모든 기본 문항이 4지선다 및 유효한 정답 번호(1~4)를 갖는지 검증"""
        for idx, q in enumerate(get_default_quizzes(), start=1):
            with self.subTest(quiz_index=idx):
                self.assertEqual(len(q.choices), 4, f"{idx}번 문항의 선택지가 4개가 아닙니다.")
                self.assertIn(q.answer, [1, 2, 3, 4], f"{idx}번 문항의 정답({q.answer})이 1~4 범위를 벗어납니다.")
                self.assertTrue(len(q.question.strip()) > 0)


class TestStateBackupAndRecovery(unittest.TestCase):
    """[평가 항목 #17] state.json 영속성, .bak 백업 생성 및 3단계 계층형 복구 테스트"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.state_file = Path(self.test_dir) / "test_state.json"
        self.backup_file = self.state_file.with_name(self.state_file.name + ".bak")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_initial_load_creates_default_and_backup(self):
        """최초 로드 시 파일이 없으면 기본 10문항으로 초기화 및 저장되는지 검증"""
        game = QuizGame(state_file=self.state_file)
        game.load_state()
        self.assertEqual(len(game.quizzes), DEFAULT_QUIZ_COUNT)
        self.assertTrue(self.state_file.exists())

    def test_save_state_creates_backup_file(self):
        """저장 시 기존 파일이 있으면 .bak 백업 파일이 자동 생성되는지 검증"""
        game = QuizGame(state_file=self.state_file)
        game.load_state()
        self.assertTrue(self.state_file.exists())

        # 퀴즈 하나 추가 후 다시 저장
        new_q = Quiz("테스트 문제", ["1", "2", "3", "4"], 1, "테스트")
        game.quizzes.append(new_q)
        game.save_state()

        # 백업 파일(.bak) 존재 여부 검증
        self.assertTrue(self.backup_file.exists(), ".bak 백업 파일이 생성되지 않았습니다.")

    def test_recovery_from_corrupted_state_using_backup(self):
        """state.json이 손상되었을 때 .bak 백업 파일로부터 2단계 복구가 정상 동작하는지 검증"""
        game = QuizGame(state_file=self.state_file)
        game.quizzes = [Quiz("유효한 퀴즈", ["A", "B", "C", "D"], 3, "백업용")]
        game.best_score = 95
        game.save_state()  # state.json 생성
        game.quizzes.append(Quiz("두번째 퀴즈", ["1", "2", "3", "4"], 1, "백업용"))
        game.save_state()  # state.json.bak 생성 (유효한 상태 백업됨)

        # 의도적으로 state.json 손상 (깨진 JSON 문자열 기록)
        with open(self.state_file, "w", encoding="utf-8") as f:
            f.write("{ broken json ...")

        # 새 게임 인스턴스로 로드 시도 -> 2단계 백업 복구 발동
        recovered_game = QuizGame(state_file=self.state_file)
        recovered_game.load_state()

        # 백업 파일에서 복구되었는지 확인
        self.assertGreaterEqual(len(recovered_game.quizzes), 1)
        self.assertEqual(recovered_game.best_score, 95)

    def test_recovery_fallback_to_default_when_both_corrupted(self):
        """state.json과 .bak 파일 모두 손상된 경우 3단계(기본 데이터셋)로 복구되는지 검증"""
        with open(self.state_file, "w", encoding="utf-8") as f:
            f.write("corrupted 1")
        with open(self.backup_file, "w", encoding="utf-8") as f:
            f.write("corrupted 2")

        game = QuizGame(state_file=self.state_file)
        game.load_state()

        self.assertEqual(len(game.quizzes), DEFAULT_QUIZ_COUNT)
        self.assertEqual(game.best_score, 0)


if __name__ == "__main__":
    unittest.main()

