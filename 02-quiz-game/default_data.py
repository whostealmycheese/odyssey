"""
Default Quiz Dataset Module
초기 실행 시 또는 state.json 파일이 손상되었을 때 로드되는 기본 퀴즈 데이터셋입니다.
"""

from typing import List
from quiz import Quiz


def get_default_quizzes() -> List[Quiz]:
    """기본 퀴즈 인스턴스 목록 반환 (주제별 총 10문항)"""
    return [
        # [주제 1: 개발/CS 상식]
        Quiz(
            question="Python 언어를 최초로 개발한 네덜란드 출신의 프로그래머는 누구일까요?",
            choices=["리누스 토발즈 (Linus Torvalds)", "귀도 반 로섬 (Guido van Rossum)", "제임스 고슬링 (James Gosling)", "데니스 리치 (Dennis Ritchie)"],
            answer=2,
            category="개발/CS"
        ),
        Quiz(
            question="HTTP 상태 코드 중 클라이언트의 요청이 정상적으로 '성공'했음을 알리는 코드는?",
            choices=["200 OK", "301 Moved Permanently", "404 Not Found", "500 Internal Server Error"],
            answer=1,
            category="개발/CS"
        ),
        Quiz(
            question="리눅스 터미널에서 현재 작업 중인 디렉토리의 절대 경로를 출력하는 명령어는?",
            choices=["ls", "pwd", "cd", "mkdir"],
            answer=2,
            category="개발/CS"
        ),
        Quiz(
            question="Docker 컨테이너가 종료되거나 삭제되어도 데이터를 호스트에 안전하게 영구 보존하기 위한 기술은?",
            choices=["Volume (볼륨)", "Port Forwarding (포트 매핑)", "Bridge Network (브릿지)", "Image Layer (이미지 레이어)"],
            answer=1,
            category="개발/CS"
        ),

        # [주제 2: 영화 & 문화]
        Quiz(
            question="영화 '기생충'으로 제72회 칸 영화제 황금종려상과 아카데미 4관왕을 달성한 감독은?",
            choices=["박찬욱", "봉준호", "이창동", "김기덕"],
            answer=2,
            category="영화/문화"
        ),
        Quiz(
            question="마블 시네마틱 유니버스(MCU)에서 타노스가 인피니티 건틀렛에 모으는 스톤의 총개수는?",
            choices=["4개", "5개", "6개", "7개"],
            answer=3,
            category="영화/문화"
        ),
        Quiz(
            question="영화 '인터스텔라'에서 시간 지연 현상이 극심하게 발생했던 바다 행성의 이름은?",
            choices=["밀러 행성", "만 행성", "에드먼즈 행성", "쿠퍼 행성"],
            answer=1,
            category="영화/문화"
        ),

        # [주제 3: 일반 상식]
        Quiz(
            question="지구 대기 중에서 약 78%로 가장 높은 비율을 차지하고 있는 기체는?",
            choices=["산소 (O2)", "이산화탄소 (CO2)", "질소 (N2)", "아르곤 (Ar)"],
            answer=3,
            category="일반상식"
        ),
        Quiz(
            question="컴퓨터의 2진수 체계에서 1바이트(Byte)는 몇 비트(Bit)로 구성될까요?",
            choices=["4 비트", "8 비트", "16 비트", "32 비트"],
            answer=2,
            category="일반상식"
        ),
        Quiz(
            question="세종대왕이 훈민정음을 반포한 서기 연도는 언제일까요?",
            choices=["1392년", "1446년", "1592년", "1418년"],
            answer=2,
            category="일반상식"
        )
    ]
