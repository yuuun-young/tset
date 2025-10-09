# --- Gemini 분석 함수 (디버깅 및 최종 수정 버전) ---
# @st.cache_data(ttl=3600) # Streamlit 환경이 아닌 경우 이 줄은 주석 처리하거나 제거하세요.
def get_gemini_analysis(ticker, info, reddit_topics, positive_mentions_examples):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "오류: 'GEMINI_API_KEY'가 설정되지 않았습니다."

    # 1. 모델 이름을 최신 버전으로 명확히 지정합니다.
    # gemini-1.5-pro-latest: 고성능 모델
    # gemini-1.5-flash-latest: 더 빠르고 경제적인 모델
    model_name = "gemini-1.5-pro-latest" 
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    # 2. (핵심) 실제로 어떤 URL로 요청이 나가는지 터미널에 출력하여 확인합니다.
    print("--- Gemini API 요청 정보 ---")
    print(f"요청 URL: {url}")
    print("--------------------------")


    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"""
    당신은 월스트리트의 유능한 금융 분석가입니다. 제공된 데이터를 바탕으로 소매 투자자를 위한 종합적인 주식 분석 보고서를 작성해 주세요. 전문적이면서도 이해하기 쉬운 언어를 사용해 주세요. 모든 최종 보고서 내용은 반드시 한국어로 작성해 주세요.

    **분석 대상 종목: {info.get('longName', ticker)} ({ticker})**
    **1. 기업 개요:**
    {info.get('longBusinessSummary', '정보 없음')}
    **2. 핵심 재무 지표:**
    - 시가총액: {info.get('marketCap', 0) / 1_000_000_000:.2f}B USD
    - PER: {info.get('trailingPE', 'N/A')}
    - PBR: {info.get('priceToBook', 'N/A')}
    - 부채비율: {info.get('debtToEquity', 'N/A')}
    **3. Reddit 커뮤니티 핵심 토픽:**
    - {', '.join(reddit_topics)}
    **4. 소셜 미디어(Reddit) 긍정적 언급 예시:**
    {''.join([f"- '{mention[:200]}...'\\n" for mention in positive_mentions_examples])}
    ---
    **[분석 보고서 요청]**
    위 정보를 바탕으로 아래 형식에 맞춰 분석 보고서를 작성해 주세요.
    **1. 투자 요약 (Executive Summary):** 2~3문장 요약
    **2. 긍정적 투자 포인트 (Bull Case):** 성장 동력, 투자 이유
    **3. 주요 리스크 (Bear Case):** 잠재적 위험, 우려 사항
    **4. 최종 결론:** 종합 의견 및 적합한 투자자 유형
    **주의:** 이 분석은 투자 추천이 아니며, 정보 제공을 목적으로 합니다.
    """
    
    data = { "contents": [ { "parts": [ { "text": prompt } ] } ] }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() 
        # 응답 구조 확인 및 안전한 데이터 추출
        candidates = response.json().get('candidates', [])
        if candidates and 'content' in candidates[0] and 'parts' in candidates[0]['content']:
            return candidates[0]['content']['parts'][0].get('text', '오류: 응답에서 텍스트를 찾을 수 없습니다.')
        else:
            return f"오류: 예상치 못한 Gemini API 응답 형식입니다.\n응답 내용: {response.text}"
            
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP 오류 발생: {http_err}\n응답 내용: {http_err.response.text}"
    except Exception as e:
        return f"Gemini 분석 보고서 생성 중 알 수 없는 오류 발생: {e}"
