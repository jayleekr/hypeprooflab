# HypeProof Lab AI Agent Orchestration System

**Version**: 1.0.0 (Phase 1 MVP)
**Last Updated**: 2026-01-22
**Status**: Phase 1 Complete

---

## 개요

HypeProof Lab AI Agent Orchestration System은 Claude AI를 활용한 지능형 에이전트 오케스트레이션 시스템입니다. 이 시스템은 독립적인 컨텍스트를 가진 여러 AI 에이전트를 조율하여 복잡한 작업을 효율적으로 처리합니다.

### 핵심 특징

- **컨텍스트 격리**: 각 에이전트는 독립적인 컨텍스트 윈도우를 유지
- **병렬 실행**: asyncio 기반 비동기 에이전트 실행
- **YAML 기반 설정**: 코드 변경 없이 에이전트 및 워크플로우 설정
- **구조화된 로깅**: JSON 형식의 로그와 API 키 자동 보호
- **품질 보증**: TRUST 5 프레임워크 기반 테스트 및 검증

---

## 아키텍처

### 3-Layer 구조

```
┌─────────────────────────────────────┐
│        Commands Layer               │  ← 사용자 인터페이스
│   (/research, /podcast, etc.)       │
├─────────────────────────────────────┤
│        Skills Layer                 │  ← 오케스트레이션
│   (DeepResearch, ContentCreation)   │
├─────────────────────────────────────┤
│        Agents Layer                 │  ← 실행 엔진
│   (Research, Analysis, Writing)     │
└─────────────────────────────────────┘
```

### Phase 1 (MVP) 구현 컴포넌트

#### Core Infrastructure
- **types.py**: Pydantic 기반 데이터 모델
  - `ExecutionStatus`: 실행 상태 (SUCCESS, ERROR, TIMEOUT)
  - `TokenUsage`: 토큰 사용량 추적
  - `AgentResult`: 에이전트 실행 결과
  - `AgentConfig`: 에이전트 설정
  - `SkillConfig`: 스킬 설정 (Phase 1.5)

- **logger.py**: 구조화된 JSON 로깅
  - API 키 자동 스크러빙
  - structlog 기반 구조화된 로그
  - 타임스탬프 및 로그 레벨 자동 추가

- **error_handler.py**: 중앙화된 에러 처리
  - 커스텀 예외 타입 (HypeProofError, AgentExecutionError, ConfigurationError, TimeoutError)
  - 구조화된 에러 응답
  - 재시도 가능 에러 판별

- **config_loader.py**: YAML 설정 로더
  - agents.yaml 파싱 및 검증
  - settings.yaml 로딩
  - Pydantic 기반 설정 검증

- **registry.py**: 에이전트/스킬 레지스트리
  - 싱글톤 패턴 에이전트 인스턴스 관리
  - 동적 에이전트 등록 및 조회
  - 의존성 주입 지원

#### Agents
- **base_agent.py**: 모든 에이전트의 기반 클래스
  - Claude SDK 통합
  - 독립적 컨텍스트 관리
  - 실행 시간 및 토큰 추적
  - 에러 처리 및 로깅

- **research_agent.py**: 웹 검색 전문 에이전트
  - WebSearch 및 WebFetch 도구 사용
  - 구조화된 리서치 결과 반환
  - 신뢰도 평가 및 출처 표시

#### Commands
- **research.py**: /research 명령 핸들러
  - ResearchAgent 오케스트레이션
  - 사용자 입력 검증
  - CLI 및 API 인터페이스 제공

---

## 설치 및 설정

### 필수 요구사항

- Python 3.11+ (권장) 또는 3.9+
- pip (Python 패키지 관리자)

### 의존성 설치

```bash
# 프로젝트 디렉토리로 이동
cd hypeproof

# 의존성 설치
pip install -r requirements.txt

# 개발 의존성 설치 (테스트용)
pip install -r requirements-dev.txt
```

### 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가하세요:

```env
# Claude API 설정
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# 로깅 설정
LOG_LEVEL=INFO
LOG_FORMAT=json

# 에이전트 설정
DEFAULT_MODEL=claude-sonnet-4-20250514
MAX_RETRIES=3
TIMEOUT=300

# 병렬 실행 설정
MAX_PARALLEL_AGENTS=3
```

---

## 사용 방법

### 1. Python 스크립트에서 사용

```python
import asyncio
from src.commands.research import ResearchCommand

async def main():
    # Research 명령 초기화
    command = ResearchCommand()

    # 리서치 실행
    result = await command.handle({
        "topic": "Latest AI trends in 2025"
    })

    # 결과 출력
    print(f"Status: {result['status']}")
    print(f"Findings: {result['result']}")
    print(f"Execution time: {result['execution_time']}s")

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. CLI에서 사용

```bash
# Research 명령 실행
python -m src.commands.research "Latest AI trends in 2025"
```

### 3. 에이전트 직접 사용

```python
import asyncio
from src.agents.research_agent import ResearchAgent

async def main():
    # 에이전트 초기화
    agent = ResearchAgent()

    # 작업 실행
    result = await agent.execute(
        task="Research quantum computing breakthroughs",
        context={"focus": "recent papers"}
    )

    # 결과 확인
    if result.status == "success":
        print(f"Output: {result.output}")
        print(f"Tokens used: {result.token_usage.total_tokens}")
    else:
        print(f"Error: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 설정 파일

### agents.yaml

에이전트 설정을 정의합니다:

```yaml
agents:
  research_agent:
    name: "Research Agent"
    role: "Web search and information gathering"
    tools:
      - Read
      - WebSearch
      - WebFetch
    max_retries: 3
    timeout: 300
    model: "claude-sonnet-4-20250514"
```

### settings.yaml

시스템 전역 설정:

```yaml
system:
  environment: "development"
  log_level: "INFO"
  default_model: "claude-sonnet-4-20250514"
  max_parallel_agents: 3
  enable_parallel: true
```

---

## 테스트

### 테스트 실행

```bash
# 전체 테스트 실행
python3 -m pytest tests/ -v

# 커버리지 포함 테스트
python3 -m pytest tests/ --cov=src --cov-report=html

# 특정 모듈 테스트
python3 -m pytest tests/test_core/test_registry.py -v
```

### 현재 테스트 커버리지

- **총 커버리지**: 47%
- **logger.py**: 100%
- **types.py**: 97%
- **registry.py**: 81%
- **base_agent.py**: 51%

---

## 프로젝트 구조

```
hypeproof/
├── src/
│   ├── core/                   # 핵심 인프라
│   │   ├── types.py           # 데이터 모델
│   │   ├── logger.py          # 로깅 시스템
│   │   ├── error_handler.py   # 에러 처리
│   │   ├── config_loader.py   # 설정 로더
│   │   └── registry.py        # 레지스트리
│   ├── agents/                # 에이전트 구현
│   │   ├── base_agent.py      # 기반 클래스
│   │   └── research_agent.py  # 리서치 에이전트
│   ├── commands/              # 명령 핸들러
│   │   └── research.py        # /research 명령
│   └── skills/                # 스킬 (Phase 1.5)
├── config/                    # 설정 파일
│   ├── agents.yaml
│   └── settings.yaml
├── tests/                     # 테스트
│   ├── conftest.py           # pytest 설정
│   ├── test_core/            # Core 테스트
│   ├── test_agents/          # Agent 테스트
│   └── test_commands/        # Command 테스트
├── docs/                      # 문서
│   ├── architecture.md       # 아키텍처 문서
│   └── ai_agent_system.md    # 이 문서
├── .moai/specs/               # SPEC 문서
├── pyproject.toml            # 프로젝트 설정
├── pytest.ini                # pytest 설정
└── requirements.txt          # 의존성
```

---

## Phase 1 완료 상태

### ✅ 구현 완료

- [x] Core Infrastructure (types, logger, error_handler, config_loader, registry)
- [x] BaseAgent 추상 클래스
- [x] ResearchAgent 구현
- [x] /research 명령 핸들러
- [x] YAML 설정 파일 (agents.yaml, settings.yaml)
- [x] 테스트 인프라 (pytest, fixtures, 기본 테스트)
- [x] 구조화된 로깅 및 API 키 보호
- [x] 에러 처리 및 복구

### 📋 다음 단계 (Phase 1.5)

- [ ] 추가 에이전트 (AnalysisAgent, WritingAgent, ReviewAgent)
- [ ] BaseSkill 오케스트레이터
- [ ] ContentCreation 및 DeepResearch 스킬
- [ ] ParallelExecutor (asyncio.gather 기반)
- [ ] /podcast 명령
- [ ] 통합 테스트 및 85% 커버리지 달성

---

## 개발 가이드라인

### TRUST 5 프레임워크

1. **Testable**: 모든 모듈은 테스트 가능해야 합니다
2. **Readable**: 코드는 자체 문서화되어야 합니다
3. **Unified**: 일관된 코딩 스타일 및 패턴
4. **Secured**: API 키 보호 및 보안 검증
5. **Trackable**: 구조화된 로깅 및 메트릭

### 코드 스타일

- **Type Hints**: 모든 함수 및 메서드에 타입 힌트 필수
- **Docstrings**: Google 스타일 독스트링 사용
- **Formatting**: Black 포매터 사용
- **Linting**: Ruff 린터 사용

---

## 문제 해결

### 일반적인 오류

1. **ModuleNotFoundError: claude_agent_sdk**
   - 테스트 환경에서는 자동으로 mock됨
   - 실제 환경에서는 claude-agent-sdk 설치 필요

2. **ImportError**
   - `pip install -r requirements.txt` 실행
   - Python 버전 확인 (3.9+)

3. **Logging errors**
   - `ANTHROPIC_API_KEY` 환경 변수 설정 확인
   - LOG_LEVEL 설정 확인

---

## 라이선스

HypeProof Lab © 2026

---

## 연락처

- 이슈 보고: GitHub Issues
- 문서: `docs/` 디렉토리 참조
- SPEC: `.moai/specs/SPEC-001-hypeproof-lab/`

