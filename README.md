# 버블 파이낸스

키움증권HTS의 조건검색식 결과 및 종목 정보를 호출하는 프로그램



조건검색식을 실행한 결과를 얻고, 결과에 나타는 종목 차트를 얻는다. 그러기 위해선 가격이 멈춘 KST 18시 이후 마다 실행되어야한다.

<br>


## 파일 구성
```sh
.gitignore
README.md
autotest.py
bubble_dataRange.py
bubble_getfilter.py
bubble_kiwoom.py
bubble_login.py
bubble_logout.py
bubble_postfilter.py
bubble_postprice.py
bubble_postreport.py
global_var.py.sample
requirements.txt
resource/
```

<br>

## 실행 환경

* Windows10
* python 3.8(32bit⭐) 

<br>

## 실행 준비

```
키움증권 OpenAPI+ 모듈을 설치https://www.kiwoom.com/h/customer/download/VOpenApiInfoView
```

```sh
# global_var.py.sample 파일을 아래와 같이 작성할 것

# global_var.py

HOST = 'xxx.xxx.xxx.xxx'  # bubble-be host 주소
DJANGO_USER = ''          # bubble-be 접속 가능한 아이디
DJANGO_PASSWORD = ''      # 패스워드
```

<br>

## 실행

6시 이후 시각으로 조건검색식 프로그램을 실행하도록 윈도우 스케줄링 설정한다.

1. 실행(win+R)에서 taskschd.msc 실행
2. 작업 만들기 실행
   1. 일반 탭
      * 가장 높은 수준의 권한으로 실행 선택
   2. 트리거 탭
      * 매주, 월화수목금 선택
   3. 동작 탭
      * 스크립트 파일명 run.bat 입력
      * 시작위치에 프로그램 경로 C:\bubblekiwoom

