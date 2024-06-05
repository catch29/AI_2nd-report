import pandas as pd # 판다스 라이브러리 불러오기

# 지도학습데이터 로드하여 입력데이터와의 레벤슈타인 거리 계산하는 클래스 정의
class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)    # CSV 파일로드(데이터프레임)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    def find_best_answer(self, input_sentence):
        '''레베슈타인 거리 계산한 값으로 최소값 인덱스 찾아 답변 반환 '''
        def calc_distance(a, b):
            ''' 레벤슈타인 거리 계산하기 '''
            if a == b: return 0 # 같으면 0을 반환
            a_len = len(a) # a 길이
            b_len = len(b) # b 길이
            if a == "" : 
                return b_len
            if b == "" : 
                return a_len
            # 2차원 표 (a_len+1, b_len+1) 준비하기 --- (※1)
            # matrix 초기화의 예 : [[0, 1, 2, 3], [1, 0, 0, 0, 0], [2, 0, 0, 0, 0], [3, 0, 0, 0, 0], [4, 0, 0, 0, 0]]
            # [0, 1, 2, 3]
            # [1, 0, 0, 0]
            # [2, 0, 0, 0]
            # [3, 0, 0, 0] 
            matrix = [[] for i in range(a_len+1)] # 리스트 컴프리헨션을 사용하여 1차원 초기화
            for i in range(a_len+1): # 0으로 초기화
                matrix[i] = [0 for j in range(b_len+1)]  # 리스트 컴프리헨션을 사용하여 2차원 초기화
            # 0일 때 초기값을 설정
            for i in range(a_len+1):
                matrix[i][0] = i
            for j in range(b_len+1):
                matrix[0][j] = j
            # 표 채우기 --- (※2)
            #print(matrix,'----------')
            for i in range(1, a_len+1):
                ac = a[i-1]
                # print(ac,'=============')
                for j in range(1, b_len+1):
                    bc = b[j-1] 
                    # print(bc)
                    cost = 0 if (ac == bc) else 1  #  ac와 bc가 같다면 0 아니면 1
                    matrix[i][j] = min([
                        matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                        matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                        matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
                    ])
                    # print(matrix)
                # print(matrix,'----------끝')
            return matrix[a_len][b_len]
        
        distance = [] #빈 리스트 생성
        for question in self.questions :
            l_dist = calc_distance(input_sentence, question) # 입력데이터와 학습질문의 거리 계산 후 값과 질문 튜플
            distance.append((l_dist,question)) # 리스트에 거리계산값과 질문을 튜플로 추가
        # print(distance)
        # 거리를 기준으로 오름차순으로 정렬, 20번째까지 출력 - 확인용
        '''
        sorted_distances = sorted(distance, key=lambda x: x[0])[:20] 
        for dist, question in sorted_distances:
            print(f"Distance: {dist}, Question: {question}")

        '''
        # 레벤슈타인 거리 최소값의 인덱스를 찾아 답변을 반환
        best_match_index = distance.index(min(distance))
        return self.answers[best_match_index]

# CSV 파일 경로를 지정하세요.
filepath = "C:/pyjh/chatbot/ChatbotData.csv"

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)
    
