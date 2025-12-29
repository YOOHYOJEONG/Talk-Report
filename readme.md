<p align="center">
  <img src="https://github.com/YOOHYOJEONG/Talk-Report/blob/master/assert/logo.png?raw=true" width="180" alt="톡리포트 로고"/>
</p>

<h1 align="center">📊 톡리포트 — KakaoTalk Chat Analyzer</h1>

<p align="center">
  카카오톡 대화 파일(.txt)을 업로드하면 기간 및 사용자별 메시지를 분석하고 시각화를 제공하는 웹 서비스
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
</p>

---

## 💬 소개

**톡리포트(Talk Report)** 는  
카카오톡에서 내보낸 **대화 텍스트 파일(.txt)** 을 기반으로 기간별·사용자별 대화 패턴을 분석해주는 웹 기반 분석 도구입니다.

- 기간별 메시지 수 분석  
- 사용자별 메시지 수 분석  
- 시간대별 메시지 수 분석  
- 사용자별 단어 분석 (추가 예정)

---

## 🛠️ 주요 기능

### 📁 1. 파일 업로드
- 카카오톡 “대화 내보내기(.txt)” 파일 업로드

### 📅 2. 분석 기간 선택
- 시작 / 종료 날짜 및 시간 선택

### 📊 3. 분석 결과 제공
- 전체 메시지 수  
- 사용자별 메시지 수   
- 사용자별 메시지 수 순위표   
- 시간대별 메시지 그래프  
- (예정) 사용자별 단어 빈도  
---    
#### 2025.12.19 update   
- 사용자별 메시지 수 그래프를 내림차순으로 정렬하여 시각화 하도록 수정하였습니다.      
- 사용자별 메시지 수 순위를 표로 나타내도록 추가하였습니다.   
---    
#### 🆕 2025.12.29 update
- 파일 하나 선택 또는 폴더 전체 선택이 가능하도록 수정하였습니다.
- pc톡에서의 내보내기 포맷과 모바일에서의 내보내기 포맷이 달라 모두 파싱할 수 있도록 수정하였습니다.
- 전체적인 UI를 개선하였습니다.

## 🖼️ 화면 예시
<p align="center">
  <img src="https://github.com/YOOHYOJEONG/Talk-Report/blob/master/assert/example.png?raw=true" width="700" alt="톡리포트 화면 예시"/>
</p>   


## 📝 사용 방법 요약

파일 업로드 → 기간 선택 → 분석하기 → 그래프 확인

---

## 📂 프로젝트 구조

project/   
├─ app/   
│ ├─ main.py        # FastAPI 서버   
│ ├─ parser.py      # 카카오톡 로그 파서   
│ ├─ analysis.py    # 통계 분석   
│ └─ static/   
│ ├─ index.html     # UI 페이지   
│ └─ script.js      # Plotly 그래프 및 프론트 JS   
├─ assets/   
│ └─ logo.png       # 서비스 로고   
│ └─ example.png    # 동작 화면   
├─ requirements.txt   
└─ README.md   

## ⚙️ 설치 및 실행 방법

### ✔️ 1. Repository 클론

```bash
git clone https://github.com/your/repo.git
cd repo
```
   
### ✔️ 2. 패키지 설치
```bash
pip install -r requirements.txt
```    

### ✔️ 3. FastAPI 서버 실행
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
   
### ✔️ 4. 접속
브라우저에서 아래 주소로 접속 :
```bash
http://localhost:8000
```
   
