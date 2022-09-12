# 코드 설명
해당 서비스를 만드는 과정에서 사용된 코드를 정리해놓았으며, 주석을 달아 부가적인 설명을 추가하였다.

## 크롤링.ipynb
<img width="424" alt="image" src="https://user-images.githubusercontent.com/88447983/189692896-100e84c5-f960-410f-8921-2056aed7a0ef.png">
셀레니엄과 뷰티풀숲 모듈을 활용하여 '프랑스 파리'와 관련된 **브런치,블로그,여행서적** 의 글을 크롤링한다.

## 텍스트전처리.ipynb
![image](https://user-images.githubusercontent.com/88447983/189693058-b8fa087a-27e7-47ca-8cfb-42620b549244.png)  
텍스트 전처리를 통해 불용어와 특수문자를 제거 및 정제하였다. 전처리를 완료한 후, 모델 학습을 위한 데이터를 새로 저장하였다.

## 키워드추출.ipynb
![image](https://user-images.githubusercontent.com/88447983/189693252-6c69c17c-d86f-485d-a385-3fc8ceca7743.png)  
텍스트팀에서 키워드 추출을 위해 두 가지 모델을 후보로 두었었다. 하나는 응집도 기반 키워드 추출 모델이며, 다른 하나는 TF-IDF 모델이다. 우선 응집도 기반 키워드 추출 모델은 블로그 글에서는 효과적이었으나, 브런치 데이터에서는 추출을 했을 때 일상 단어를 추출하는 빈도수가 높아 키워드 추출에는 적합하지 않다는 것을 확인했다. **따라서 KoGPT2를 브런치 데이터로 파인 튜닝하고, 응집도 기반 키워드 추출모델과 PMI지수를 활용하여 (블로그와 여행 서적 텍스트 데이터를 활용하여) 출력한 키워드를 입력하면 문장을 생성하는 모델을 만들기로 결정하였다.**

- [응집도 기반 키워드 추출에 관한 논문](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/69086f34-0f11-45eb-bdca-d9604aaf810c/%EC%9D%91%EC%A7%91%EB%8F%84_%EA%B8%B0%EB%B0%98_%ED%82%A4%EC%9B%8C%EB%93%9C_%EC%B6%94%EC%B6%9C.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220912%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220912T065423Z&X-Amz-Expires=86400&X-Amz-Signature=941bf0545a79e89edcc780c7ea7595fcd2d98850b693b545fe52ba3f1fd12b86&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22%25EC%259D%2591%25EC%25A7%2591%25EB%258F%2584%2520%25EA%25B8%25B0%25EB%25B0%2598%2520%25ED%2582%25A4%25EC%259B%258C%25EB%2593%259C%2520%25EC%25B6%2594%25EC%25B6%259C.pdf%22&x-id=GetObject)
- 응집도 기반 키워드 추출 : 응집도 기반 키워드 추출은 단어의 빈도수를 기반으로 응집도 점수를 계산하여, 별도의 사전이 필요없다는 장점을 가지고 있다. 응집도 점수는 단어를 구성하는 글자들만의 정보를 이용하여 단어의 경계를 판단하는 산정 방법이다. 한국어 어절의 경우, 의미를 지니는 명사, 동사, 형용사 등의 단어에 ㅐ당하는 L파트와, 문법 기능을 위한 조사나 어미에 해당하는 R 파트로 구성되어있다. 이때 목표는 L+R 형태의 어절에서 L을 분리해내는 것이며, 응집도 점수는 이를 위한 식을 제공한다. 일반적으로, 주어진 어절이 의미가 있는 L 파트에 해당할 경우 빈도수가 높게 나타나며, 의미가 없는 R 파트를 포함할 경우 빈도수가 떨어진다.따라서 예를들어 "노란색을", "노란", "노란색", "노"와 같은 단어가 있을때, "노란색"이 키워드로 선정될 수 있도록 응집도 점수가 정의된다."노란"의 경우도 키워드로 선정될 수 있으나, 빈도가 비슷하게 나타날 경우 일반적으로 긴 단어가 더 풍부한 의미를 지닌다는 사실로부터 "노란색"이 선정될 수 있도록 응집도 점수를 정의한다.

**키워드 추출 결과**  

![image](https://user-images.githubusercontent.com/88447983/189693440-849e3129-a1f5-42b8-9404-50d3187134ed.png)

![image](https://user-images.githubusercontent.com/88447983/189693810-92891e99-be80-47d8-a4ac-7b000eb24363.png)  
키워드 연관성을 파악하기 위해 PMI지수를 사용했고, 최종적으로 응집도로 추출한 키워드와 연관성 결과를 비교하여 후보 키워드를 산정하였다.

## 텍스트생성기_kogpt2_finetuning.ipynb
<img width="563" alt="image" src="https://user-images.githubusercontent.com/88447983/189690640-259b8bc8-bef0-42dd-adc7-b93928afdfb8.png">
추출된 키워드를 바탕으로 KoGPT2를 이용하여 텍스트 생성을 진행했다. 여행기 텍스트의 문체를 학습시키기 위해 브런치 데이터를 사용하였으며, epoch 및 파라미터를 조정하여 fine-tuning의 과정을 거쳤다. 출력 문장이 길수록, 문장이 뒤로 갈수록 연관성과 정확도가 떨어지는 문제가 있었으나, 학습 데이터를 늘리고, 정확도 향상을 위해 전처리 과정을 보완하여 성능을 향상시킬 수 있었다.
![image](https://user-images.githubusercontent.com/88447983/189680084-f5560aa9-2e04-4565-867c-5448cfcbec54.png)
- KoGPT2 : GPT-2 모델을 fine-tuning한 한국어 언어모델이며, SKT-AI에서 한국어 성능 한계 개선을 위해 개발하였다. KoGPT2는 2020년 2월에 개발된 KoGPT1의 업그레이드 버전이다. 1에서는 단일 문장 생성에 최적화되었지만, 2에서는 문맥을 유지하며 다중 문장 생성에 최적화되어 의미적으로 연관된 문단을 생성할 수 있다. 
- 이 모델은 GPT-2와 마찬가지로 논문 Attention Is All You Need에서 제시한 인코더+디코더 구조에서 인코더 블록을 제거하고 디코더 블록만 사용한 모델이다. 그렇지만 Transformer은 그 목적이 번역을 잘 하는것이었기에 영어를 Encode하고, 다시 프랑스어로 Decode하는 과정이 필요했기 때문에 Encoder, Decoder가 필요했던 것이다. 하지만, BERT와 GPT는 그 목적이 언어 모델을 사전학습 시키는 것이기 때문에 Encoding과 Decoding의 과정이 필요하지 않는다.  


![image](https://user-images.githubusercontent.com/88447983/189694033-a030a3b9-a421-4663-af27-e87d4c90d60a.png)  
100 epoch 학습 결과 손실률은 0.019로 높은 정확도를 보여주었다.  
![image](https://user-images.githubusercontent.com/88447983/189694221-76c1683a-8a4f-4ae7-9cae-fc921ec82c59.png)  
다음은 텍스트 생성 함수로 키워드와 최대 출력 길이를 입력으로 받는다.  


## 제목추출.ipynb  
![image](https://user-images.githubusercontent.com/88447983/189694526-f6a12b04-c13e-46ac-b65a-fbe507de4c10.png)  
텍스트 요약 모델 GPT3를 사용하여 제목 생성을 진행한다.

## 사극_말투학습모델.ipynb
![image](https://user-images.githubusercontent.com/88447983/189695557-59076c08-0978-45eb-9d11-9a9ef33e8cab.png)
![image](https://user-images.githubusercontent.com/88447983/189695622-4812af10-178d-468b-b9c5-3a409395b9c8.png)
![image](https://user-images.githubusercontent.com/88447983/189695661-69379afb-58c6-4352-a5b3-841a15ce30ba.png)

트랜스포머 모델의 학습데이터로 사극 대본을 선정하였다. 일반 문장을 입력하였을 때 성경 말투로 습을 시키는 방법이 올라와있는 깃허브를 이용하려고 했으나, 실제로 모델이 작동하지 않아 팀에서 비슷한 방법으로 모델을 생성하였다.그 결과 "오늘은 빨리 달려 가야겠다"를 입력하였을때, "오늘은 속히 달리어 갈 것이다."가 출력됨을 확인하였다. 이를 이용하여 일반 평서체에서 사극말투를 학습하였다.  
TTS 엔진토큰화 된 문장이 입력값이 되면 부자연스러운 음성이 합성되기 때문에 말투 학습 후 나온 출력문장에서는 토큰화된 형태로 출력되어 일반 문장으로 변환할 필요가 있었다.
