# 뉴스 요약봇 만들기

## 프로젝트 소개

영어 뉴스 기사에서 짧은 요약을 만드는 두 가지 방법을 비교했습니다. 추상적 요약은 어텐션 기반 seq2seq 모델로 새 헤드라인을 생성하고, 추출적 요약은 Summa의 TextRank로 기사에서 중요한 문장을 뽑습니다. 기사 본문과 원본 헤드라인이 있는 `news_summary_more.csv`를 사용했습니다.

12에포크 학습 후 검증 손실은 3.1673에서 2.1356으로 감소했습니다. 같은 테스트 기사 200건에서 원본 헤드라인의 핵심 단어를 얼마나 포함했는지 비교한 결과, 평균 회수율은 추상적 요약 48.24%, 추출적 요약 56.24%였습니다. 이 중 8건은 문법 완성도와 내용도 직접 비교했습니다.

[뉴스 요약봇 만들기 노트북](./뉴스_요약봇_만들기.ipynb)에서 전처리 코드, 학습 그래프, 비교 표를 확인할 수 있습니다. 다시 실행하려면 Colab에서 GPU를 선택하고 위에서부터 모든 셀을 실행하면 됩니다.

## Project overview

This project compares two ways to summarize English news articles. An attention-based seq2seq model writes new headlines, and Summa TextRank picks important sentences from the articles. The project uses the articles and original headlines in `news_summary_more.csv`.

Validation loss fell from 3.1673 to 2.1356 after 12 epochs. On the same 200 test articles, the generated headlines recovered 48.24% of the original headline keywords on average, and the extracted summaries recovered 56.24%. We also reviewed eight examples for grammar and content.

The [project notebook](./뉴스_요약봇_만들기.ipynb) includes the preprocessing code, training graph, and comparison tables. To rerun it, select a GPU in Colab and run all cells from top to bottom.

---

# Peer Review Templete
- 코더 : 코더의 이름을 작성하세요.
- 리뷰어 : 리뷰어의 이름을 작성하세요.


# PRT(Peer Review Template)
- [ ]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 문제에서 요구하는 최종 결과물이 첨부되었는지 확인
        - 중요! 해당 조건을 만족하는 부분을 캡쳐해 근거로 첨부
    
- [ ]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 해당 코드 블럭을 왜 핵심적이라고 생각하는지 확인
    - 해당 코드 블럭에 doc string/annotation이 달려 있는지 확인
    - 해당 코드의 기능, 존재 이유, 작동 원리 등을 기술했는지 확인
    - 주석을 보고 코드 이해가 잘 되었는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부
        
- [ ]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해보았나요?**
    - 문제 원인 및 해결 과정을 잘 기록하였는지 확인
    - 프로젝트 평가 기준에 더해 추가적으로 수행한 나만의 시도, 
    실험이 기록되어 있는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부
        
- [ ]  **4. 회고를 잘 작성했나요?**
    - 주어진 문제를 해결하는 완성된 코드 내지 프로젝트 결과물에 대해
    배운점과 아쉬운점, 느낀점 등이 기록되어 있는지 확인
    - 전체 코드 실행 플로우를 그래프로 그려서 이해를 돕고 있는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부
        
- [ ]  **5. 코드가 간결하고 효율적인가요?**
    - 파이썬 스타일 가이드 (PEP8) 를 준수하였는지 확인
    - 코드 중복을 최소화하고 범용적으로 사용할 수 있도록 함수화/모듈화했는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부


# 리뷰어 회고(참고 링크 및 코드 개선 제안)
    # 리뷰어의 회고를 작성합니다.
    # 코드 리뷰 시 참고한 링크가 있다면 링크와 간략한 설명을 첨부합니다.
    # 코드 리뷰를 통해 개선한 코드가 있다면 코드와 간략한 설명을 첨부합니다.