# Chapter02-02-wordGame

## 준비
```bash
pip install -r requirements.txt
```
- `.env`에 `OPENAI_API_KEY`를 설정합니다.
- `data/words_vectors.pkl`이 없으면 `preprocess/get_vectors.py`를 실행해 생성합니다. (OpenAI 임베딩 사용)

## 실행
```bash
streamlit run web.py
```
- 단어를 입력해 정답 단어와의 유사도를 확인하고, 힌트를 바탕으로 추리합니다.
- 사이드바의 개발용 체크박스로 정답 확인이 가능합니다.

## 종료
- 터미널에서 `Ctrl + C`로 서버를 중지합니다.

