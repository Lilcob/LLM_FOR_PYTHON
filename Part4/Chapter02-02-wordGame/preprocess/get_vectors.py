from dotenv import load_dotenv
import os
import pickle
import unicodedata
import re
from typing import Set
import time
from openai import OpenAI

# OpenAI 클라이언트 인스턴스화
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 한글 단어 여부 확인 함수
def is_hangul(text) -> bool:
    return bool(re.match(r'^[\u3130-\u318F\uAC00-\uD7A3]+$', text))

# 단어 로드
def load_dic(path: str) -> Set[str]:
    rtn = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            word = line.strip()
            word = unicodedata.normalize('NFC', word)
            if is_hangul(word):
                rtn.add(word)
    return list(rtn)

# OpenAI API를 통한 벡터 생성 함수
def get_embedding(word, model="text-embedding-3-small"):
    response = client.embeddings.create(
        input=word,
        model=model,
        dimensions = 10
    )
    return response.data 

# 단어 벡터 딕셔너리 생성
def create_word_vector_dict(word_list):
    word_vecs = {}
    emb_vectors = get_embedding(word_list)
    for idx,vec in enumerate(emb_vectors):
        if vec is not None:
            word_vecs[word_list[idx]] = vec.embedding
    return word_vecs

# 벡터를 파일로 저장
def save_word_vectors(word_vecs, save_path):
    with open(save_path, 'wb') as file:
        pickle.dump(word_vecs, file)
    print(f"✅ 단어 벡터가 '{save_path}'에 저장되었습니다.")

# 파일 경로 설정
wordlist_path = '../data/words_dataset.txt'
save_path = '../data/words_vectors.pkl'

# 실행
print("📥 단어 사전 로딩 중...")
normal_words = load_dic(wordlist_path)
print(f"총 {len(normal_words)}개의 한글 단어 로드 완료.")

print("🔍 임베딩 벡터 생성 중 (OpenAI API 사용)...")
word_vecs = create_word_vector_dict(normal_words)

print("💾 벡터 저장 중...")
save_word_vectors(word_vecs, save_path)

print("완료")
# print(word_vecs)
