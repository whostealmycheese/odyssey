"""
Quiz Model Module
개별 퀴즈를 표현하고 출제, 정답 검증 및 직렬화(JSON 변환)를 담당하는 모델 클래스입니다.
"""

from typing import List, Dict, Any


class Quiz:
    """개별 퀴즈를 표현하는 클래스"""

    def __init__(self, question: str, choices: List[str], answer: int, category: str = "개발/CS"):
        """
        Quiz 객체 초기화
        :param question: 문제 지문
        :param choices: 선택지 목록 (기본 4지선다)
        :param answer: 정답 번호 (1부터 시작하는 정수)
        :param category: 퀴즈 주제 분류 (기본값: 개발/CS)
        """
        self.question: str = question
        self.choices: List[str] = choices
        self.answer: int = answer
        self.category: str = category

    def display(self, q_num: int) -> None:
        """
        문제를 콘솔에 서식에 맞추어 출력
        :param q_num: 문제 번호
        """
        print(f"\n[{q_num}번 문제 | 주제: {self.category}]")
        print(f"Q. {self.question}\n")
        for idx, choice in enumerate(self.choices, start=1):
            print(f"  {idx}. {choice}")
        print()

    def is_correct(self, user_answer: int) -> bool:
        """
        사용자가 선택한 번호가 정답과 일치하는지 판별
        :param user_answer: 사용자가 입력한 번호 (1~4)
        :return: 정답 여부 (True / False)
        """
        return user_answer == self.answer

    def to_dict(self) -> Dict[str, Any]:
        """
        JSON 파일 저장을 위해 딕셔너리로 직렬화
        :return: 퀴즈 데이터 딕셔너리
        """
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Quiz":
        """
        딕셔너리 데이터로부터 Quiz 인스턴스 역직렬화 생성
        :param data: JSON에서 로드한 딕셔너리
        :return: Quiz 객체
        """
        return cls(
            question=data.get("question", ""),
            choices=data.get("choices", []),
            answer=data.get("answer", 1),
            category=data.get("category", "일반 상식")
        )

    def __repr__(self) -> str:
        return f"<Quiz [{self.category}] {self.question[:15]}... ans={self.answer}>"
