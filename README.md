# youth-policy-mcp

온통청년 OPEN API를 실시간 호출하는 Python 기반 MCP HTTP 서버입니다. FastMCP의 `streamable-http` transport를 사용하며 기본 endpoint는 `/mcp`입니다. API 응답은 MCP client가 읽기 쉽도록 사람이 이해하기 쉬운 필드명으로 정규화합니다.

## 제공 도구

- `search_youth_policies`: 청년 정책 목록 검색. 내부적으로 `pageType=1`을 사용합니다.
- `get_youth_policy_detail`: 정책번호 기반 상세 조회. 내부적으로 `pageType=2`, `plcyNo=policy_id`를 사용합니다.
- `check_policy_eligibility`: 사용자 조건과 정책 조건을 비교한 예비 신청 가능성 판단입니다.
- `compare_youth_policies`: 여러 정책의 지원내용, 신청기간, 자격조건, 신청방법, 제출서류, 기관 정보를 비교합니다.
- `build_policy_application_checklist`: 특정 정책 신청 준비 체크리스트를 생성합니다.

## 환경변수

API 키는 코드에 포함하지 않고 환경변수로만 전달합니다.

```bash
YOUTH_CENTER_API_KEY=your_api_key_here
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_TRANSPORT=streamable-http
```

선택 환경변수:

```bash
YOUTH_CENTER_API_URL=https://www.youthcenter.go.kr/opi/youthPlcyList.do
YOUTH_CENTER_TIMEOUT_SECONDS=15
```

온통청년 API 문서에서 endpoint가 바뀐 경우 `YOUTH_CENTER_API_URL`만 바꾸면 됩니다.

## 로컬 실행

Python 3.11 기준입니다.

```bash
cd youth-policy-mcp
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`.env` 파일에 `YOUTH_CENTER_API_KEY`를 설정한 뒤 실행합니다.

```bash
export YOUTH_CENTER_API_KEY=your_api_key_here
export MCP_HOST=0.0.0.0
export MCP_PORT=8000
export MCP_TRANSPORT=streamable-http
python -m src
```

Windows PowerShell에서는 다음처럼 설정할 수 있습니다.

```powershell
$env:YOUTH_CENTER_API_KEY="your_api_key_here"
$env:MCP_HOST="0.0.0.0"
$env:MCP_PORT="8000"
$env:MCP_TRANSPORT="streamable-http"
python -m src
```

서버 URL:

```text
http://localhost:8000/mcp
```

## Docker 실행

```bash
docker build -t youth-policy-mcp .
docker run --env-file .env -p 8000:8000 youth-policy-mcp
```

컨테이너 내부 포트는 `8000`입니다.

## 외부 MCP 클라이언트 등록값

GitHub에 올린 뒤 Dockerfile 기반으로 이미지를 빌드하고 배포한 경우 MCP 서버 등록 페이지에는 보통 아래 값을 입력합니다.

- Transport: `HTTP` 또는 `Streamable HTTP`
- URL: `https://your-domain.example.com/mcp`
- Local test URL: `http://localhost:8000/mcp`
- Authentication: 없음. 단, 온통청년 API 키는 서버 환경변수 `YOUTH_CENTER_API_KEY`로만 주입합니다.
- Docker build command: `docker build -t youth-policy-mcp .`
- Docker run command: `docker run --env-file .env -p 8000:8000 youth-policy-mcp`

PlayMCP, MCP Inspector, ChatGPT의 MCP 등록 화면에서 HTTP endpoint가 필요하면 `/mcp`까지 포함한 URL을 입력하세요.

## GitHub 배포 흐름

```bash
git init
git add .
git commit -m "Initial youth policy MCP server"
git branch -M main
git remote add origin https://github.com/YOUR_ID/youth-policy-mcp.git
git push -u origin main
```

이후 배포 플랫폼에서 GitHub repository를 연결하고 Dockerfile build를 선택합니다. 배포 환경변수에 반드시 `YOUTH_CENTER_API_KEY`, `MCP_HOST=0.0.0.0`, `MCP_PORT=8000`, `MCP_TRANSPORT=streamable-http`를 등록합니다.

## 검증

```bash
python -m compileall src
pytest
```

서버 실행 후 MCP endpoint 확인:

```bash
python -m src
```

별도 터미널에서 MCP Inspector 또는 PlayMCP로 `http://localhost:8000/mcp`에 연결합니다.

## 주의

`check_policy_eligibility`의 결과는 최종 신청 가능 여부가 아닙니다. API의 텍스트 조건이 애매하거나 사용자가 충분한 정보를 제공하지 않은 경우 `needs_review` 또는 `insufficient_information`을 반환하며, 정책 공고문과 담당 기관 확인을 안내합니다.
