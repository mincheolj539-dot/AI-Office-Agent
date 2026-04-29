import streamlit as st
import os
from PyPDF2 import PdfReader
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI

# --- 1. 기능 함수 정의 ---
def upload_pdf(file_uploaded):
    reader = PdfReader(file_uploaded)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

def extract_content(pdf_text, max_length=15000): 
    # Gemini는 똑똑해서 더 긴 글(15,000자)도 거뜬히 읽습니다!
    if len(pdf_text) > max_length:
        pdf_text = pdf_text[:max_length] + "\n...[이하 생략]..."
    return pdf_text

def summarize_content(llm, pdf_text):
    prompt = f"다음 문서를 분석하고 핵심 내용을 3~5줄로 요약해 주세요:\n\n{pdf_text}"
    result = llm.invoke(prompt)
    return result.content

def write_email(llm, summary):
    prompt = f"다음 요약 내용을 바탕으로 거래처에 보낼 정중한 비즈니스 이메일 초안을 작성하세요:\n\n{summary}"
    result = llm.invoke(prompt)
    return result.content

def save_results(summary, email_body, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("요약: \n")
        f.write(summary)
        f.write("\n\n이메일 초안: \n")
        f.write(email_body)

# --- 2. 메인 UI 로직 ---
if __name__ == "__main__":
    st.set_page_config(page_title="AI Office Agent", page_icon="🔥")
    st.title("AI Office Agent")

    # 사이드바 API 키 입력
    st.sidebar.title("API 설정")
    api_key = st.sidebar.text_input(label="Google Gemini API Key를 입력하세요", type="password")
    st.sidebar.info("위 텍스트 칸에 api키를 입력해 주시오")

    # API 키가 입력되었을 때만 구글 AI 준비
    llm = None
    if api_key:
        try:
            # 🚨 404 에러가 나던 폐기된 이름을 버리고, 현재 구글에서 공식 지원하는 최신 2.5 모델로 교체!
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
            st.sidebar.success("API 키가 확인되었습니다")
        except Exception as e:
            st.sidebar.error(f"오류: {e}")
    else:
        st.warning("왼쪽 사이드바에 API 키를 먼저 입력해 주세요.")

    # 파일 업로드 섹션
    uploaded_file = st.file_uploader("PDF 파일 업로드", type=["pdf"])

    # 파일이 업로드되었고, API 키(llm)가 준비되었을 때만 실행
    if uploaded_file is not None and llm is not None:
        if st.button("분석 시작"):
            with st.spinner("AI가 문서를 분석 중입니다..."):
                try:
                    # 내용 분석(추출)
                    pdf_text = upload_pdf(uploaded_file)
                    extracted_text = extract_content(pdf_text)

                    # 요약 및 메일 작성
                    summary = summarize_content(llm, extracted_text)
                    email_body = write_email(llm, summary)

                    # 파일 자동 저장
                    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
                    os.makedirs("agent_results", exist_ok=True)
                    filename = os.path.join("agent_results", f"result_{current_datetime}.txt")
                    save_results(summary, email_body, filename)

                    # 결과 화면 출력
                    st.subheader("요약 결과:")
                    st.write(summary)
                    
                    st.divider()
                    
                    st.subheader("이메일 초안:")
                    st.write(email_body)
                    
                    st.success(f"💾 결과가 `{filename}`에 성공적으로 저장되었습니다.")
                except Exception as e:
                    st.error(f"실행 중 오류가 발생했습니다: {e}")