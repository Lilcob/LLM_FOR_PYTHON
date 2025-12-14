import streamlit as st
import pickle
import random
import pandas as pd 
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity

# ① 단어 벡터 딕셔너리 로드 함수
def load_word_vectors(pickle_path):
    with open(pickle_path, 'rb') as file:
        return pickle.load(file)

# ② 단어 임베딩 정보 및 단어 가져오기
pickle_path = './data/words_vectors.pkl'
word_vector_dict = load_word_vectors(pickle_path)
words =list(word_vector_dict.keys())

# ③ 페이지 설정 및 제목 설정
st.set_page_config(
    page_title="단어 추리 게임",
    layout="centered"
)
st.title("단어 추리 게임")

# ④ 유저의 입력(단어 정보) 제어
    # 입력창 초기화
def submit():
    st.session_state.user_input = st.session_state.input_box
    st.session_state.input_box = ""

# ⑤ 단어 간의 유사도를 계산하는 함수 
def calculate_similarity(guess, target, word_vecs):
    # 새로운 단어와 랜덤 단어의 벡터를 가져오기
    guess_word_vec = word_vecs.get(guess)
    target_word_vec = word_vecs.get(target)
    # 코사인 유사도 계산 
    similarity = cosine_similarity([guess_word_vec], [target_word_vec])
    # -1에서 1 사이의 유사도를 0에서 100 사이로 변환
    similarity = (similarity + 1) * 50
    return similarity[0][0]

# ⑥ 세션 상태 초기화 (게임 상태 유지를 위해)
    # 정답 단어 정보 초기화
if 'target_word' not in st.session_state:
    # 정답 단어 랜덤 추출
    st.session_state.target_word = random.choice(words)
    st.session_state.guesses = []
    st.session_state.messages = ""
    # 유사도 저장을 위한 딕셔너리 추가
    st.session_state.similarities = {}
    # 단어 입력 순서 저장
    st.session_state.order_counter = 0

    # 유저 입력 상태 초기화
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
     
# ⑦ 유저의 입력 (단어 정보) 제어
    # 유저 입력 UI

st.text_input(
    "단어를 입력하세요:",
    value="",  # 항상 빈 값으로 시작
    placeholder="단어를 입력해주세요",
    key="input_box",
    on_change=submit
)


# ⑧ 입력한 단어와 정답 단어간의 유사도 계산 및 결과 확인
user_text = st.session_state.user_input
# 입력 처리
if user_text:
    # 입력한 단어 공백 제거 처리
    guess = user_text.strip()
    # 유저가 입력한 단어에 대한 처리
    if guess in st.session_state.guesses: # 이미 입력했던 단어 처리
        st.session_state.messages = f"'{guess}'는 이미 시도한 단어입니다."
    elif guess not in word_vector_dict: # 유사도 계산할 수 없는 단어 처리
        st.session_state.messages = f"'{guess}'는 단어장에 없는 단어입니다."  
    else: #유사도 계산 및 결과 확인 
        st.session_state.order_counter += 1
        
        # 유사도 계산
        similarity = calculate_similarity(guess, st.session_state.target_word, word_vector_dict)
        
        # streamlit session 내 단어와 유사도 저장
        st.session_state.guesses.append(guess)
        st.session_state.similarities[guess] = {
            "order": st.session_state.order_counter,
            "similarity": similarity
        }
        
        if guess == st.session_state.target_word: 
            st.session_state.messages = f"🎉 정답입니다! '{guess}'를 맞추셨습니다!"
            st.balloons()
        else:
            # 간단한 힌트 제공
            if similarity > 0.7:
                st.session_state.messages = f"'{guess}'는 정답이 아닙니다. 하지만 매우 가깝습니다!"
            elif similarity > 0.5:
                st.session_state.messages = f"'{guess}'는 정답이 아닙니다. 하지만 꽤 가깝습니다."
            elif similarity > 0.3:
                st.session_state.messages = f"'{guess}'는 정답이 아닙니다. 어느 정도 가깝습니다."
            else:
                st.session_state.messages = f"'{guess}'는 정답이 아닙니다. 많이 멀었습니다."
    # #입력창 초기화
    st.session_state.user_input = ""

# ➈ 게임 기록 시각화
# 텍스트 표시 공간
st.subheader("게임 기록")
st.text(st.session_state.messages)

# 시도한 단어 목록을 표 형태로 시각화
if st.session_state.guesses:
    st.subheader("시도한 단어 목록")
    # 데이터프레임 생성
    data = []
    for word in st.session_state.guesses:
        data.append({
            "단어": word,
            "유사도": f"{st.session_state.similarities[word]['similarity']:.2f}"
        })
    # 데이터프레임으로 변환
    df = pd.DataFrame(data)
    # 유사도를 기준으로 내림차순 정렬
    df = df.sort_values(by="유사도", ascending=False)
    # 정렬된 데이터프레임 표시
    st.dataframe(df, use_container_width=True)

# ⑩ 게임 재시작 설정
if st.button("게임 다시 시작"):
    # 이전 게임의 정답을 messages에 추가
    st.session_state.messages = f"정답은 '{st.session_state.target_word}'였습니다. \n새 게임이 시작되었습니다!"
    # st.text(st.session_state.messages)
    # 게임 상태 초기화
    st.session_state.target_word = random.choice(words)
    st.session_state.guesses = []
    st.session_state.similarities = {}
    st.session_state.order_counter = 0
    # 화면 새로 고침
    st.rerun()
    
# 개발 중에만 사용할 정답 확인 (실제 게임에서는 제거)
if st.sidebar.checkbox("정답 보기 (개발용)"):
    st.sidebar.write(f"현재 정답: {st.session_state.target_word}")