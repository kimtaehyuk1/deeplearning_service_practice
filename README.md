|문장생성|챗봇|
|:-:|:-:|
|<img src="https://user-images.githubusercontent.com/67897827/223158500-33b3ff0b-4237-40fe-9804-40bef87bc1db.PNG" width="700" height="300"/>|<img src="https://user-images.githubusercontent.com/67897827/223158509-ba07cc3a-c404-466c-81a3-c311a642b3ce.PNG" width="700" height="300"/>| 


# 1. 딥러닝을 활용하여 문장생성 및 챗봇기능을 탑재하여 웹서비스 구현. 
KoGTP2를 이용하여 문장생성,챗봇구현 후 웹서비스 띄우기


## 개발 순서
1. 로컬에서 개발(vs code)
    - kogpt모델 사용 생성기능, 챗봇기능
    - 웹 서비스 구현(프론트는 adminLTE 필요소스.)
2. 클라우드 환경 배포
    - AWS 가상서버 생성
    - 가상서버 제어 위한 MobaXterm(퍼블릭 IP와, 개인키 필요) -> MobaXterm 폴더생성후 코드 구현 소스 복사 -> 실행

## 작동 흐름도
- 웹 -> 입력 -> 서버로 전송 -> 토크나이저를 이용하여 인코딩 -> 모델에 주입 -> 예측(생성,챗봇) -> 디코딩 -> 응답

### 참고
- adminLTE 에서 zip소스파일 다운후 static넣기 -> 가져와서 경로 맞추기 헤더 : href="/static/plugins/ , /static/dist
- 바디 : src="/static/plugins/
- adminLTE url : https://github.com/ColorlibHQ/AdminLTE/releases/tag/v3.2.0

- 학습을 마친 모델을 가져와 사용하는데, 학습한 모델을 불러올시 깃 푸쉬가 안되는 문제로 run.py를 가동 할때만 넣고 깃에는 푸쉬안함.

---------------------
밑에는 클라우드에서 가상서버 만든 후 MobaXterm에서 설치한 것.
```
[처음 접속했으므로 우분트 s.w 최신으로 패치]
- 패키지들의 레퍼지토리 주소를 최신업데이트
$ sudo apt-get update
- 최신 버전 설치
$ sudo apt-get upgrade
---------------------------------------------------
가상 환경 구축을 위한 패키지 설치
$ sudo apt-get install python3-venv
가상 환경 구축:web:가상환경이름
$ python3 -m venv web
가상 환경 활성화
$ source ./web/bin/activate
프럼프트가 가상환경으로 변경됨
(web)$

필요 패키지 설치 (CPU only)
(web)$ pip install transformers[torch] --no-cache-dir
(web)$ pip install transformers[tf-cpu] --no-cache-dir
(web)$ pip install flask flask-socketio

or

(web)$ pip install transformers --no-cache-dir
(web)$ pip install tensorflow --no-cache-dir
(web)$ pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
(web)$ pip install flask flask-socketio

- 폴더 생성 f
- 소스 업로드 run.py, templates 폴더
- 보안그룹에 사용자 정의 TCP 3333 모든 위치에서 접근 가능하도록 추가
- (web)$ python ./f/run.py
- 브라우저 접속 및 요청 및 테스트
  - http://본인퍼블릭IP:3333
```
