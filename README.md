# AI Office Agent (AI 기반 문서 자동 분석 및 비즈니스 메일 작성 툴)

LangChain과 Google Gemini API를 활용한 사내 문서 처리 업무 자동화 파이프라인 구축 프로젝트입니다.

## Tech Stack
- **Language:** Python
- **UI Framework:** Streamlit
- **AI Framework:** LangChain
- **API & LLM:** Google Gemini API (2.5 Flash)
- **Library:** PyPDF2

## Key Features (주요 구현 사항)
- LangChain `PromptTemplate` 기반의 다단계(Multi-step) AI 파이프라인을 구축하여 문서 요약 및 비즈니스 메일 연쇄 작성 자동화.
- `PyPDF2`를 통한 텍스트 파싱 및 LLM 컨텍스트 윈도우 초과 방지를 위한 텍스트 청킹(Chunking) 적용으로 데이터 전처리 프로세스 최적화.
- 사용자 개인 API 키를 웹 UI 환경(Sidebar)에서 동적으로 입력받아 세션을 유지하도록 설계하여 하드코딩으로 인한 보안 이슈 차단.
- 최종 분석 결과와 이메일 초안을 타임스탬프 기반의 텍스트(.txt) 파일로 지정된 로컬 디렉토리(`agent_results/`)에 자동 생성 및 보존하는 파일 I/O 처리.

## Troubleshooting (트러블슈팅)
**1. 로컬 하드웨어 병목 현상 및 아키텍처 전환**
- **Issue:** 초기에는 데이터 보안을 위해 로컬 LLM(Ollama 기반 Llama 3.2)을 채택했으나, 다량의 PDF 텍스트 파싱 시 심각한 메모리 과부하 및 추론 속도 저하 발생.
- **Solution:** 연산 주체를 로컬에서 클라우드로 전환. Google Gemini API를 도입하여 서버 부하를 제거하고 처리 속도를 획기적으로 단축시킴.

**2. API 버전 업데이트에 따른 Endpoint 에러 대응**
- **Issue:** 클라우드 LLM 마이그레이션 과정에서 구버전 모델(`gemini-1.5-flash`, `gemini-pro`) 폐기 정책으로 인한 `404 Not Found` 에러 발생.
- **Solution:** API 공식 문서를 디버깅하여 현재 지원되는 최신 공식 모델(`gemini-2.5-flash`)로 모듈을 즉각 마이그레이션하여 서비스 안정성 복구.

## How to Run (실행 방법)
```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 애플리케이션 실행
python -m streamlit run app.py