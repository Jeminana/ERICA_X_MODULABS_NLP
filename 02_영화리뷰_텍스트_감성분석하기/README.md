# 네이버 영화리뷰 텍스트 감성분석

Sentiment Analysis of Naver Movie Reviews

NSMC 리뷰를 전처리하고 평균 풀링, CNN, LSTM 및 Word2Vec 초기화 CNN을 비교한다.

This project cleans NSMC movie reviews and compares average pooling, CNN, LSTM, and a CNN initialized with Word2Vec embeddings.

[프로젝트 노트북 / Project notebook](%E1%84%8B%E1%85%A7%E1%86%BC%E1%84%92%E1%85%AA%E1%84%85%E1%85%B5%E1%84%87%E1%85%B2_%E1%84%90%E1%85%A6%E1%86%A8%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3_%E1%84%80%E1%85%A1%E1%86%B7%E1%84%89%E1%85%A5%E1%86%BC%E1%84%87%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%E1%86%A8%E1%84%92%E1%85%A1%E1%84%80%E1%85%B5%5B%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%8C%E1%85%A6%E1%86%A8%E1%84%90%E1%85%B3%5D.ipynb)

## 평가기준과 근거

| 평가기준 | 결과 및 근거 |
| --- | --- |
| 한국어 Word2Vec 활용, 정확도 85% 이상 | 8절 CNN_Word2Vec 테스트 정확도 **86.49%** |
| gensim 유사어로 자체학습 / 사전학습 임베딩 비교 | 7절 분류기 Embedding, 8절 직접 학습한 Word2Vec, 9절 동일 질의어 비교 및 해석 |
| 세 가지 이상 모델 성공적으로 시도 | 5절 GlobalAveragePooling, CNN, LSTM의 학습 및 검증 출력 |

외부 `word2vec_ko.model`이 제공되지 않아 강의 코드를 직접 Word2Vec을 학습하는 방식으로 수정했다.
NSMC 학습 분할로 Word2Vec을 먼저 학습한 다음 CNN 임베딩을 초기화하고 미세조정했다.
여기서 **사전학습은 감성 분류기 학습 전에 수행한 Word2Vec 학습**을 뜻한다.
외부 말뭉치에서 사전학습된 모델을 사용했다는 의미는 아니다. 추가 외부 파일은 필요하지 않다.

### Simple English: Evaluation Criteria

| Criterion | Evidence |
| --- | --- |
| Use Korean Word2Vec and reach at least 85% accuracy | Section 8: CNN_Word2Vec test accuracy is **86.49%** |
| Compare learned and pretrained embeddings using gensim similar words | Section 7: classifier embeddings; Section 8: custom Word2Vec; Section 9: shared word queries and analysis |
| Successfully train at least three model types | Section 5: training and validation outputs for GlobalAveragePooling, CNN, and LSTM |

The external `word2vec_ko.model` file was not provided, so I adapted the lecturer's code to train Word2Vec myself.
I trained Word2Vec on the NSMC training split, then used its vectors to initialize and fine-tune the CNN.
Here, **pretraining means training Word2Vec before training the sentiment classifier**.
The model uses NSMC text, rather than an external text collection. No extra pretrained model file is needed.

## 저장된 실험 결과

| 모델 | 검증 정확도 | 검증 손실 | 테스트 정확도 |
| --- | ---: | ---: | ---: |
| GlobalAveragePooling | 84.60% | 0.358842 | — |
| CNN (무작위 임베딩) | 85.82% | 0.325472 | — |
| LSTM | 86.01% | 0.333235 | 85.49% |
| CNN + NSMC Word2Vec | **86.93%** | **0.310330** | **86.49%** |

Word2Vec CNN은 무작위 초기화 CNN보다 검증 정확도가 **1.12%p** 높았다.
LSTM 테스트 값은 중간 기준 모델 평가이며, 마지막에는 검증 정확도로 선택한 CNN_Word2Vec을 평가했다.
위 수치는 기존 노트북 저장 출력에 근거한다. 이번 수정에서 학습을 재실행한 결과는 아니다.

### Simple English: Saved Results

| Model | Validation Accuracy | Validation Loss | Test Accuracy |
| --- | ---: | ---: | ---: |
| GlobalAveragePooling | 84.60% | 0.358842 | - |
| CNN (random embeddings) | 85.82% | 0.325472 | - |
| LSTM | 86.01% | 0.333235 | 85.49% |
| CNN + NSMC Word2Vec | **86.93%** | **0.310330** | **86.49%** |

Word2Vec improved CNN validation accuracy by **1.12 percentage points**.
The LSTM test score came from an earlier baseline evaluation. The final CNN_Word2Vec model was selected using validation accuracy.
These numbers come from saved notebook outputs. Training was not rerun during this update.

## 전처리와 모델

1. 중복 및 결측 제거, MeCab 형태소 분석과 불용어 제거
2. 최대 10,000개 어휘로 정수 인코딩
3. 길이 47로 post-padding/truncation (학습 리뷰 95.23% 포함)
4. 학습 파일을 80:20 계층 분할 (`random_state=42`)
5. 평균 풀링 / CNN / LSTM 학습, 검증 손실 기준 조기 종료 및 최적 가중치 복원
6. 학습 분할만으로 100차원 skip-gram Word2Vec 학습 후 CNN 초기화 및 미세조정
7. 검증 정확도로 최종 모델 선택 후 테스트 평가

전처리 후 학습 파일은 146,182건, 테스트는 49,157건이며 학습/검증은 116,945 / 29,237건이다.
어휘와 최대 길이는 검증 분리 전에 결정했다. 더 엄격한 검증에서는 분할 이후 학습 데이터만으로 정해야 한다.

### Simple English: Data Preparation and Models

1. Remove duplicate and missing reviews, tokenize with MeCab, and remove stopwords.
2. Convert words to integer IDs using a vocabulary of up to 10,000 tokens.
3. Pad or trim sequences at the end to a length of 47. This keeps 95.23% of training reviews without trimming.
4. Split the training file into 80% training and 20% validation data, keeping the label balance (`random_state=42`).
5. Train average pooling, CNN, and LSTM models. Stop early based on validation loss and restore the best weights.
6. Train a 100-dimensional skip-gram Word2Vec model using only the training split, then initialize and fine-tune the CNN.
7. Select the final model using validation accuracy and evaluate it on the test set.

After cleaning, the training file has 146,182 reviews and the test file has 49,157 reviews.
The training and validation splits contain 116,945 and 29,237 reviews.
The vocabulary and maximum sequence length were chosen before the validation split. For stricter validation, choose these using only the training split.

## 임베딩 비교와 해석

분류기 Embedding에서 ‘별로’는 ‘최악’, ‘재미없’과 가까워 부정 감성을 반영했다.
직접 사전학습한 Word2Vec에서 ‘영화’는 ‘작품’, ‘공포물’, ‘애니메이션’과 가까워 문맥 관계를 보였다.
‘재미’와 ‘재미없’도 가까울 수 있으므로 문맥 유사도가 감성 일치를 뜻하지는 않는다.
노트북 9절은 두 임베딩을 gensim으로 변환해 동일 질의어의 `most_similar()` 결과를 비교한다.

### Simple English: Embedding Comparison

In the classifier embeddings, the Korean word for "not good" was close to words meaning "worst" and "not fun", showing negative sentiment.
In the custom Word2Vec embeddings, "movie" was close to "work", "horror movie", and "animation", showing related contexts.
Words meaning "fun" and "not fun" can also be close, so similar contexts do not always mean the same sentiment.
Section 9 compares both embeddings with the same Korean query words using gensim's `most_similar()`.

## 실행 및 제출 확인

1. TensorFlow, gensim, pandas, NumPy, matplotlib, scikit-learn 및 MeCab을 사용할 수 있는 커널에서 실행한다.
2. NSMC 파일은 Colab의 `/content`, 그 외 환경에서는 현재 작업 폴더에 준비한다. 준비 셀은 없는 파일을 다운로드한다.
3. 기존 Python 3.13 Linux의 MeCab 빌드 오류는 `python-mecab-ko-py313` 설치로 해결했다.
4. 셀을 순서대로 실행한다. Word2Vec은 직접 학습하며 `word2vec_ko_custom.model`로 저장한다.
5. 새 9절 비교표와 10절 점검표를 실행하고 출력을 포함해 저장한다. 비교 결과는 `embedding_neighbours.csv`로도 저장된다.

기존 학습과 최종 테스트 출력은 보존했다. 새 비교 및 점검 셀은 아직 실행되지 않았다.
현재 로컬 환경에는 TensorFlow와 gensim이 없어 전체 학습을 재실행하지 않았다.
제출 전 기존 학습 환경에서 새 셀을 실행하고 점검표를 확인한다.

### Simple English: Running and Submission

1. Use an environment with TensorFlow, gensim, pandas, NumPy, matplotlib, scikit-learn, and MeCab.
2. Use `/content` for the NSMC files on Colab, or the current working folder elsewhere. The setup cell downloads missing files.
3. The MeCab build error in the previous Python 3.13 Linux run was fixed by installing `python-mecab-ko-py313`.
4. Run the cells in order. The custom Word2Vec model is trained and saved as `word2vec_ko_custom.model`.
5. Run the new comparison in Section 9 and the checklist in Section 10. Save the notebook with the outputs. The comparison is also saved as `embedding_neighbours.csv`.

The existing training and final test outputs have been kept. The new comparison and checklist cells have not been run yet.
The local environment does not have TensorFlow or gensim, so full training was not rerun.
Before submitting, run the new cells in the original training environment and check the results.

## 회고 및 동료 리뷰

외부 모델이 없는 상황에서 강의 코드를 직접 사전학습 방식으로 수정했다.
후속 개선 과제는 여러 시드에서 성능 개선의 안정성을 확인하고 검증 분리 이후 어휘를 구성하는 것이다.
마스킹 평균 풀링은 패딩을 제외하고 분모의 최솟값을 1로 제한하여 빈 리뷰의 0 나눗셈을 방지한다.

리뷰어 이름과 캡처는 실제 리뷰 후 추가한다.

- [ ] 최종 결과와 평가기준 근거 확인 (5절, 8~10절)
- [ ] 핵심 코드의 주석과 동작 확인
- [ ] 설치 오류 해결 및 Word2Vec 추가 실험 확인
- [ ] 결과 해석과 회고 확인 (9절, 11절)
- [ ] 코드 간결성과 재사용성 확인

### Simple English: Reflection and Peer Review

I adapted the lecturer's code to train Word2Vec because the external model was not available.
Future improvements include checking results with several random seeds and building the vocabulary after splitting the data.
The masked average pooling layer ignores padding and keeps the denominator at least 1 to avoid division by zero for empty reviews.

Add the reviewer's name and screenshots after the actual review.

- [ ] Check the final results and evaluation evidence (Sections 5 and 8-10).
- [ ] Check the comments and behavior of the main code.
- [ ] Check the installation fix and extra Word2Vec experiment.
- [ ] Check the result analysis and reflection (Sections 9 and 11).
- [ ] Check that the code is clear and reusable.
