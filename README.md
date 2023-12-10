# ShowMeTheMoney

### 💰로또

#### 기능 요구사항

🔥 로또가 정규분포를 따를 것이라고 가정하고, 로또구매에 참여한다.
(또한 위 가정의 옳음을 확률적으로 분석한다.)

1. 1회차에 5 Round에 참여한다. (5000원)
2. 각 Round 마다 45개 중 6개의 번호를 뽑는다.

🔥 분석 방법 
1. 7.5개 마다 1개의 번호를 뽑는다. => (번호 분포 기대값 : 7.5)
2. 6개 번호의 합은 138에 가까워야 함. => (합의 평균 기대값 : 138)
3. 각 번호의 출현 확률은 동일해야 함. => (모든 번호의 우선순위가 같다면, 가장 적게 출현한 번호를 우선으로 선택)

...

😁 기타 분석(?) 방법
1. 홀짝 -> 3개씩 출현한다..?
2. 고저 -> 중간인 23을 기준으로 상하 3개씩 출현한다..?

----
 
#### 비기능 요구사항

1. 매 주 토요일, 6개의 번호가 갱신된다.

   - 로컬 dataset에 해당 번호 Update
   - github의 lotto/dataset/lotto_data.csv 경로에 최신화.
   - 최신화 데이터를 이용하여 5 round 번호 추출

2. 매 주 금요일, 5 round (5000원)을 구매한다.

   - 5000원 결제 기능

3. 웹사이트에 당첨결과 업로드

----

#### Lotto Dataset

|Id|DataType|
|:---|---:|
|Round|Integer|
|Date|String|
|1stNum|Integer|
|2ndNum|Integer|
|3rdNum|Integer|
|4thNum|Integer|
|5thNum|Integer|
|6thNum|Integer|
|BonusNum|Integer|
