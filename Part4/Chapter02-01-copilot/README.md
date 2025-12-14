# Chapter02-01-copilot

## 준비
```bash
pip install -r requirements.txt
```
- `.env`에 API 키를 설정합니다.  
  - `gemini_api_key` (Gemini용 `app.py`)  
  - `openai_api_key` (OpenAI용 `Copilot_openai.py`)

## 실행
- Gemini 기반:
```bash
streamlit run app.py
```
- (추가)OpenAI 기반:
```bash
streamlit run Copilot_openai.py
```
- 작업을 선택해 번역 또는 코드 수정 기능을 실행합니다.

## 종료
- 터미널에서 `Ctrl + C`로 서버를 중지합니다.

