import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Gemini API 테스트")
st.title("🧪 Gemini API 단독 호출 테스트")
st.write("이 앱은 다른 기능 없이 오직 Gemini API 연결만 테스트합니다.")

# --- 1. API 키 설정 테스트 ---
st.subheader("1. API 키 설정 테스트")
try:
    # Streamlit Secrets에서 API 키를 불러옵니다.
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("오류: Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. [Settings] > [Secrets]를 확인하세요.")
    else:
        genai.configure(api_key=api_key)
        st.success("성공: Gemini API 키가 정상적으로 설정되었습니다!")
        
except Exception as e:
    st.error(f"API 키 설정 중 오류 발생: {e}")
    st.info("API 키 값 자체에 오타가 없는지, Google AI Studio에서 키가 활성화되어 있는지 확인하세요.")


# --- 2. API 호출 테스트 ---
st.subheader("2. API 직접 호출 테스트")

# API 키가 성공적으로 설정되었을 때만 버튼을 활성화합니다.
if 'api_key' in locals() and api_key:
    if st.button("Gemini API에 질문하기"):
        try:
            with st.spinner("Gemini 모델을 호출하는 중..."):
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                response = model.generate_content("하늘이 파란 이유를 간단히 설명해줘.")
                
                st.success("🎉 API 호출 성공!")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"API 호출 중 심각한 오류 발생: {e}")
            st.warning("Google Cloud 프로젝트에서 'Vertex AI API'가 활성화되었는지, 또는 결제 계정에 문제가 없는지 확인해보세요.")
else:
    st.warning("API 키가 설정되지 않아 테스트를 진행할 수 없습니다.")
