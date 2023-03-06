'''
    - 필요 패키지 설치
    - pip install tensorflow
    - pip install transformers
        - 맥북 계열은 아래 방식 참고
        - https://jamescalam.medium.com/hugging-face-and-sentence-transformers-on-m1-macs-4b12e40c21ce
    - pip install flask-socketio
    - conda install pytorch
'''
from flask import Flask, render_template, jsonify, request
import tensorflow as tf
from transformers import AutoTokenizer
from transformers import TFGPT2LMHeadModel
import numpy as np
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
# 실시간 통신(SocketIO 사용)을 위해 비밀키 지정
app.config['SECRET_KEY'] = 'kimtaehyuk'  # 임의의 키값을 지정
socketio = SocketIO(app)

# 문장 생성 관련 모델
repo = 'skt/kogpt2-base-v2'
sent_tokenizer = AutoTokenizer.from_pretrained( repo )
model = TFGPT2LMHeadModel.from_pretrained( repo, from_pt=True )

# 챗봇 모델
repo = './gpt_chatbot'
tokenizer = AutoTokenizer.from_pretrained(repo)
chatbot_model = TFGPT2LMHeadModel.from_pretrained(
    repo)  # 이미 텐서플로우 모델이므로 from_pt 배제


def request_answer_by_chatbot(text):
  bos = [tokenizer.bos_token_id]
  sentence = bos + \
      tokenizer.encode(f'{tokenizer.decode(2)}{text}{tokenizer.decode(4)}')
  sent_tensor = tf.convert_to_tensor([sentence])
  answer = chatbot_model.generate(
      sent_tensor, max_length=50, top_k=3, do_sample=True)
  answer = tokenizer.decode(answer[0].numpy().tolist())
  return answer.split('<sys>')[1].split('</s>')[0]


# 라우팅을 하지 않으면 -> 404 오류 발생
@app.route('/')
def home():
    return render_template('index_.html')

# 문장 생성 페이지


@app.route('/nlp/create_sentence')
def create_sentence():
    return render_template('pages/create_sentence.html',info={'title': '문장생성 v1'})

# 챗봇 페이지

@app.route('/nlp/chatbot')
def chatbot():
    # info라는 파라미터는 개발자가 지정한 파라미터(설정)
    return render_template('pages/chatbot.html', info={'title': '챗봇 v1'})

# 챗봇 질문에 대한 답변 처리


@app.route('/nlp/chatbot_proc', methods=['POST'])
def chatbot_proc():
    # 추후 딥러닝 모델을 추가해서 응답을 동적으로 예측(문장생성) 하여 처리한다.
    question = request.form.get('msg')  # 사용자의 질문을 추출
    answer = request_answer_by_chatbot(question)  # 질문 넣서 모델 예측후 답변생성
    res = {'answer': answer, 'name': '관리자'}
    return jsonify(res)

# 클라이언트 메시지를 처리하기 위한 이벤트 등록및 처리


@socketio.on('cTos_simple_msg')
def cTos_simple_msg(data):
    print(data)
    # echo, 받는 내용을 살짝 수정해서 응답(서버 => 클라이언트로 메시지 전송, 푸시)
    data['msg'] += "<응답"
    emit('sToc_simple_msg', data)


@socketio.on('cTos_create_sentence')
def cTos_create_sentence(data):
    seed_sentence = data['seed']  # 받은거에서 seed인덱싱해서(줄떄 키를 seed로 줬으니)
    print('문장생성의 재료 문장 획득', seed_sentence)
    # 1. 문장 -> 인코딩(벡터화)
    input_vectors = sent_tokenizer.encode(seed_sentence)
    # 2. 제한된 문장 길이만큼 다음 토큰을 예측해서 클라이언트로 푸시
    while len(input_vectors) < 50:  # 전체 문장이 30토큰이 되면 종료 설정.
        output = model(np.array([input_vectors]))  # 다음꺼 예측
        # 입력문자 토큰 4개중에 마지막 토큰의 인덱스 번호 -1만 선택 => 마지막 토큰에 대한 다음에 올 토큰 후보 51200개만 추춣
        top5 = tf.math.top_k(output.logits[0, -1], k=5)
        # top5를  선택하는 방식이 달라지면 문장의 내용도 달라짐
        token_id = random.choice(top5.indices.numpy())
        # 모델이 예측한 다음 토큰을 추가하여 문장을 계속 이어나가고 이를 기반으로 다음 토큰을 곘고 예측 수행한다.
        input_vectors.append(token_id)  # input_vectors은 리스트니까
        # 클라이언트에게 예측 토큰 전송
        emit('sToc_create_sentence', {'word': sent_tokenizer.decode([token_id]), 'name':'관리자'})


if __name__ == '__main__':
    #app.run()
    # 소켓IO를 지원하는 기반 서버 가동
    socketio.run(app, port=3333, debug=True)
