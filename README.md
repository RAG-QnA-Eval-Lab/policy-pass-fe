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

### 테스트

```bash
pytest
```

## 배포 (CI/CD)

### Step 1: Daehyun(인프라 담당)에게 받아야 할 것

| 항목 | 설명 |
|------|------|
| AWS Secret Access Key | `toby` IAM 사용자의 Secret Key (대면 전달) |
| App Runner 서비스 ARN | `rag-qa-ui` 서비스의 ARN |
| API 서비스 URL | 백엔드 App Runner 서비스 URL (`API_BASE_URL`에 필요) |

### Step 2: AWS CLI 프로필 설정

```bash
aws configure --profile rag-qa
# AWS Access Key ID: Daehyun에게 문의
# AWS Secret Access Key: Daehyun에게 문의
# Default region name: ap-northeast-2
# Default output format: json
```

검증:
```bash
aws sts get-caller-identity --profile rag-qa
# Account: 355206939988 이 나와야 함
```

### Step 3: GitHub Secrets 등록

레포 → **Settings** → **Secrets and variables** → **Actions**:

| Secret Name | 값 | 설명 |
|-------------|-----|------|
| `AWS_ACCESS_KEY_ID` | Daehyun에게 문의 | AWS IAM Access Key |
| `AWS_SECRET_ACCESS_KEY` | Daehyun에게 문의 | AWS IAM Secret Key |
| `APPRUNNER_SERVICE_ARN` | Daehyun에게 문의 | App Runner UI 서비스 ARN |

### Step 4: 로컬 Docker 빌드 테스트

```bash
docker build -t rag-ui .
docker run -p 8501:8501 -e API_BASE_URL=http://host.docker.internal:8080 rag-ui
# http://localhost:8501 접속 → Streamlit UI 표시
```

### 배포 흐름

```
main 브랜치에 push (또는 수동 트리거)
    ↓
GitHub Actions 실행
    ↓
Docker 이미지 빌드
    ↓
ECR (rag-ui)에 push
    ↓
App Runner 자동 재배포
```

- **main 브랜치에 push하면 자동 배포됩니다**
- PR을 먼저 만들고 리뷰 후 머지하세요
- 수동 배포: GitHub → Actions 탭 → Run workflow

### 배포 시 환경변수

App Runner 서비스에서 아래 환경변수가 설정됩니다 (인프라 담당이 관리):

| 변수 | 값 |
|------|-----|
| `API_BASE_URL` | `https://{API App Runner 서비스 URL}` |

## 주의사항

- **API 백엔드가 먼저 배포되어 있어야 합니다** → `API_BASE_URL`이 유효해야 함
- **시크릿을 코드에 하드코딩하지 마세요** → `.env` 사용
- **`.env` 파일은 절대 커밋하지 마세요** → `.gitignore`에 포함되어 있습니다

## 관련 레포

| 레포 | 역할 |
|------|------|
| [policy-pass-be](https://github.com/RAG-QnA-Eval-Lab/policy-pass-be) | FastAPI 백엔드 |
| [policy-pass-infra-aws](https://github.com/RAG-QnA-Eval-Lab/policy-pass-infra-aws) | AWS 인프라 설정 |
| [policy-pass-datapipeline-gcp](https://github.com/RAG-QnA-Eval-Lab/policy-pass-datapipeline-gcp) | GCP 데이터 파이프라인 |
