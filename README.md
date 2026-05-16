# Policy Pass — Frontend

청년정책 RAG QA 시스템의 React 프론트엔드입니다.

## 기술 스택

- **React 19** + **TypeScript 5**
- **Vite 6** (빌드 & 개발 서버)
- **ESLint 9** (린팅)

## 프로젝트 구조

```
policy-pass-fe/
├── src/
│   ├── main.tsx              # 엔트리포인트
│   ├── App.tsx               # 루트 컴포넌트
│   ├── index.css             # 글로벌 스타일
│   └── vite-env.d.ts         # Vite 환경변수 타입
├── index.html                # HTML 템플릿
├── package.json              # 의존성 관리
├── tsconfig.json             # TypeScript 설정
├── vite.config.ts            # Vite 설정
├── .env.example              # 환경변수 템플릿
└── .github/workflows/
    └── deploy.yml            # CI/CD (S3 배포 → CloudFront 캐시 무효화)
```

## 로컬 개발 환경 설정

### 1. Node.js 설치

Node.js 20 이상이 필요합니다. [nvm](https://github.com/nvm-sh/nvm) 사용을 권장합니다.

```bash
nvm install 20
nvm use 20
```

### 2. 의존성 설치

```bash
npm install
```

### 3. 환경변수 설정

```bash
cp .env.example .env
# .env 파일에서 VITE_API_BASE_URL을 설정하세요
```

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `VITE_API_BASE_URL` | 백엔드 API 주소 | `http://localhost:8080` |

### 4. 백엔드 먼저 실행

프론트엔드는 [policy-pass-be](https://github.com/RAG-QnA-Eval-Lab/policy-pass-be)에 의존합니다.
백엔드를 먼저 실행한 뒤 프론트엔드를 시작하세요.

```bash
# 다른 터미널에서 백엔드 실행
cd ../policy-pass-be
uvicorn src.api.main:app --reload --port 8080
```

### 5. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 `http://localhost:3000` 접속

## 주요 명령어

| 명령어 | 설명 |
|--------|------|
| `npm run dev` | 개발 서버 (HMR, port 3000) |
| `npm run build` | 프로덕션 빌드 (`tsc` + `vite build`) |
| `npm run preview` | 빌드 결과물 미리보기 |
| `npm run lint` | ESLint 실행 |

## API 연동

백엔드 API 호출 시 `VITE_API_BASE_URL` 환경변수를 사용합니다:

```typescript
const API_BASE = import.meta.env.VITE_API_BASE_URL;

const response = await fetch(`${API_BASE}/ask`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: '청년 주거 정책' }),
});
const data = await response.json();
```

## 배포

main 브랜치에 머지되면 GitHub Actions가 자동으로 배포합니다:

1. `npm ci` → `npm run build`
2. `dist/` → S3 버킷 동기화 (해시된 에셋은 `immutable` 캐시, `index.html`은 `no-cache`)
3. CloudFront 캐시 무효화

## 브랜치 작업 규칙

**main 브랜치에 직접 push하지 마세요.** 반드시 브랜치를 만들어서 작업하고 PR로 머지합니다.

```bash
# 1. 작업 브랜치 생성
git checkout -b feature/내작업이름

# 2. 코드 작성 후 커밋
git add .
git commit -m "feat: 기능 설명"

# 3. 원격에 push
git push origin feature/내작업이름

# 4. GitHub에서 PR 생성 → 리뷰 → main에 머지
```

- 브랜치 이름 예시: `feature/chat-ui`, `fix/api-connection`, `refactor/components`
- 머지 전 최신 코드 반영: `git pull origin main`
- **main에 머지되면 자동 배포됩니다** (CI/CD는 인프라 담당이 관리)

## 주의사항

- **시크릿을 코드에 하드코딩하지 마세요** → `.env` 사용
- **`.env` 파일은 절대 커밋하지 마세요** → `.gitignore`에 포함되어 있습니다
- Vite 환경변수는 반드시 `VITE_` 접두사를 붙여야 클라이언트에서 접근 가능합니다

## 관련 레포

| 레포 | 역할 |
|------|------|
| [policy-pass-be](https://github.com/RAG-QnA-Eval-Lab/policy-pass-be) | FastAPI 백엔드 |
| [policy-pass-infra-aws](https://github.com/RAG-QnA-Eval-Lab/policy-pass-infra-aws) | AWS 인프라 설정 |
| [policy-pass-datapipeline-gcp](https://github.com/RAG-QnA-Eval-Lab/policy-pass-datapipeline-gcp) | GCP 데이터 파이프라인 |
