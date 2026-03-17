# agent-bible

LangChain/LangGraph 기반 에이전트 실습 코드 모음입니다.

## 구성

- `coding_agent/`: 코드 생성/실행용 에이전트와 커스텀 툴
- `PART2/web_agent/`: 웹 검색 도구를 사용하는 에이전트 예제

## 실행 환경

- Python 3.10+
- 의존성 설치:

```bash
pip install -r requirements.txt
```

## 실행 예시

```bash
python coding_agent/agent.py
```

## requirements 갱신 CLI

```bash
python -m pip install langchain-community
python -m pip freeze > requirements.txt
```

## 메모

- 민감 정보는 `.env`에 저장하고 Git에는 포함하지 않습니다.
