# Policy Pass — Frontend (Streamlit)

청년정책 RAG QA 시스템의 Streamlit 프론트엔드입니다.

## 프로젝트 구조

```
policy-pass-fe/
├── src/
│   └── ui/
│       └── app.py            # Streamlit 엔트리포인트
├── .streamlit/
│   └── config.toml           # Streamlit 설정
├── Dockerfile                # 컨테이너 빌드 (포트 8501)
├── pyproject.toml            # 의존성 관리
├── .env.example              # 환경변수 템플릿
└── .github/workflows/
    └── deploy.yml            # CI/CD (ECR push → App Runner 배포)
```

## 로컬 개발 환경 설정

### 1. Python 환경 구성

```bash
python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 2. 환경변수 설정

```bash
cp .env.example .env
# .env 파일에서 API_BASE_URL을 설정하세요
```

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `API_BASE_URL` | 백엔드 API 주소 | `http://localhost:8080` |

### 3. 백엔드 먼저 실행

프론트엔드는 [policy-pass-be](https://github.com/RAG-QnA-Eval-Lab/policy-pass-be)에 의존합니다.  
백엔드를 먼저 실행한 뒤 프론트엔드를 시작하세요.

```bash
# 다른 터미널에서 백엔드 실행
cd ../policy-pass-be
uvicorn src.api.main:app --reload --port 8080
```

### 4. Streamlit 실행

```bash
streamlit run src/ui/app.py --server.port 8501
```

브라우저에서 `http://localhost:8501` 접속 → "API 연결 정상" 메시지 확인

## 개발 가이드

### UI 구성

`src/ui/app.py`에서 Streamlit UI를 개발하세요:

```
src/
└── ui/
    ├── app.py              # 메인 페이지
    ├── components/         # 재사용 컴포넌트
    └── pages/              # 멀티페이지 (선택)
```

### API 연동

백엔드 API 호출 시 `httpx`를 사용합니다:

```python
import httpx

r = httpx.post(f"{API_BASE_URL}/ask", json={"query": "청년 주거 정책"}, timeout=60)
data = r.json()
```

### 새 라이브러리 추가 시

새 패키지를 설치했다면 **반드시 `pyproject.toml`에 추가**해야 배포에 반영됩니다.

```toml
# pyproject.toml

dependencies = [
    "streamlit>=1.38",
    "httpx>=0.27",
    "새패키지>=1.0",          # ← 여기에 추가
]
```

> Dockerfile은 수정할 필요 없습니다. `pip install "."`이 pyproject.toml을 자동으로 읽습니다.

## 배포 전 로컬 Docker 테스트

배포 환경과 동일한 조건에서 테스트하려면 [Docker Desktop](https://www.docker.com/products/docker-desktop/)을 설치하고 아래를 실행하세요:

```bash
docker build -t rag-ui .
docker run -p 8501:8501 -e API_BASE_URL=http://host.docker.internal:8080 rag-ui
# http://localhost:8501 접속 → Streamlit UI 표시
```

> `host.docker.internal`은 Docker 컨테이너에서 호스트(로컬) 머신에 접근하는 주소입니다. 백엔드가 로컬에서 실행 중이어야 합니다.

## 배포

- **main 브랜치에 push하면 자동 배포됩니다** (CI/CD는 인프라 담당이 관리)
- PR을 먼저 만들고 리뷰 후 머지하세요

## 주의사항

- **시크릿을 코드에 하드코딩하지 마세요** → `.env` 사용
- **`.env` 파일은 절대 커밋하지 마세요** → `.gitignore`에 포함되어 있습니다

## 관련 레포

| 레포 | 역할 |
|------|------|
| [policy-pass-be](https://github.com/RAG-QnA-Eval-Lab/policy-pass-be) | FastAPI 백엔드 |
| [policy-pass-infra-aws](https://github.com/RAG-QnA-Eval-Lab/policy-pass-infra-aws) | AWS 인프라 설정 |
| [policy-pass-datapipeline-gcp](https://github.com/RAG-QnA-Eval-Lab/policy-pass-datapipeline-gcp) | GCP 데이터 파이프라인 |
