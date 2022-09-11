<img width="361" alt="image" src="https://user-images.githubusercontent.com/88447983/188566661-da6ca137-16f2-4eaf-a5ee-f7cf54dff8bb.png" width="30%" height="30%">

<img width="458" alt="image" src="https://user-images.githubusercontent.com/88447983/189523901-728d8f6d-b7b2-4d4b-9f38-fff9a5e87ac3.png">

# 키워드 추출 모델 : TF-IDF(Term Frequency-Inverse Document Frequency)
- TF : 1개의 문서안에서 특정 단어의 등장 빈도를 의미
- DF : 특정 단어가 나타나는 문서의 갯수를 의미
- IDF : 특정 단어 모든 문서에 등장하는 흔한 단어라면, 이를 방지하기 위해 TF-IDF 가중치를 낮추기 위해 역수를 취한 값
단어의 빈도(TF)와 역 문서 빈도(IDF)를 토대로, 특정 문서 내에 어떤 단어가 얼마나 중요한지를 나타내는 통계적 수치이다. 즉 단어마다 점수를 매겨서 중요도를 표시하겠다는 이론인데, 이 중요도는 문서빈도와 역문서빈도를 계산해서 둘을 곱한 결과이다. 
