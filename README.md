# Forest_hackathon

Healing effect prediction(수정 예정): 
- 기능: 산림 치유 효과(운동량 위주) 예측 
- data.csv: 산림빅데이터 거래소의 "산림치유 효과분석 건강측정정보" 데이터 
- pred: 결과 값
- 사용 모델: XGboost


Recommendation:
- 기능: 사용자 정보(성별,나이,직업)에 따라 선호 산림 체험 프로그램 추천
- input: user 정보
- db: 선호 산림 체험 검색기록, 산림체험 프로그램
- output: 산림체험 프로그램 목록 list(80개)
- 사용 모델: all-MiniLM-L6-v2
