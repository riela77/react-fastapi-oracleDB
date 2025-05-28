## 🍭 프로젝트 개요

이 프로젝트는 **React (프론트엔드)**, **FastAPI (백엔드)**, 그리고 \*\*Oracle DB (데이터베이스)\*\*를 연동하여
회원 등록 및 사용자 조회 기능을 제공하는 웹 어플리케이션입니다.

* 사용자는 아이디, 비밀번호, 프로필 이미지를 등록할 수 있습니다.
* 등록된 사용자는 Oracle DB에 저장되며, 이미지 파일은 서버에 업로드됩니다.
* 등록된 사용자 정보는 React 화면에서 실시간으로 조회할 수 있습니다.

---

## 🧱 전체 아키텍처

```
[React (LoginReg.js)]
       │        ▲
       ▼        │
[FastAPI 서버: userDAO.py]
       │        ▲
       ▼        │
[Oracle DB + 이미지 파일 시스템]
```

1. **React (프론트엔드)**

   * 사용자 입력 (아이디, 비밀번호, 프로필 이미지)
   * 회원 등록 요청: `POST /user.reg`
   * 사용자 목록 조회 요청: `GET /user.get`

2. **FastAPI (백엔드)**

   * `userDAO.py`와 `userManager.py`를 통해 DB 접근 및 파일 업로드 처리
   * 사용자 등록 시 DB에 INSERT, 프로필 이미지는 서버 디렉토리에 저장
   * 사용자 목록 조회 시 프로필 이미지 경로를 포함한 데이터 반환

3. **Oracle DB**

   * 사용자 정보를 저장 (`may27_siteUsers` 테이블)
   * 저장 컬럼: `user_id`, `user_pw`, `user_pf` (프로필 이미지 파일명)

---

## 🔄 회원 등록 흐름

1. React 컴포넌트에서 `regUser()` 함수 실행
2. FormData로 사용자 정보 전송 (`POST /user.reg`)
3. FastAPI는:

   * 프로필 이미지를 서버에 저장
   * Oracle DB에 사용자 정보 저장
4. React는 응답 받은 데이터를 이용해 화면 갱신 (회원 목록에 추가)

---

## 📁 주요 파일 설명

### ✅ React (`/site/loginReg.js`)

* 사용자 입력값 상태 관리 (`useState`)
* 프로필 사진 업로드 지원 (`input type="file"`)
* 사용자 목록 테이블 렌더링
* 서버 통신: `axios` 사용

### ✅ FastAPI (`userDAO.py`)

* `reg`: 이미지 저장 + DB INSERT 수행
* `get`: Oracle DB에서 전체 사용자 정보 SELECT

### ✅ OracleDB 테이블 구조 (`may27_siteUsers`)

| Column Name | Type    | Description |
| ----------- | ------- | ----------- |
| user\_id    | VARCHAR | 사용자 아이디     |
| user\_pw    | VARCHAR | 사용자 비밀번호    |
| user\_pf    | VARCHAR | 프로필 이미지 파일명 |

---

## 🖼 프로필 이미지 처리

* 사용자가 업로드한 이미지 파일은 서버 디렉토리에 저장됩니다.
* React에서 이미지 경로는 다음과 같이 사용됩니다:

  ```jsx
  <img src={`http://localhost:5678/user.profile.get?filename=파일명`} />
  ```
* 다운로드 링크도 제공됩니다.

---

## 🔧 기술 스택

* **Frontend**: React (CRA), Axios
* **Backend**: FastAPI (Python 3.11+)
* **Database**: Oracle 11g/12c
* **서버간 통신**: CORS 허용 설정 (`Access-Control-Allow-Origin`)

---

## 🚀 실행 방법

1. Oracle DB 준비 (테이블 `may27_siteUsers` 생성)
2. FastAPI 서버 실행

   ```bash
   uvicorn main:app --reload --port 5678
   ```
3. React 앱 실행

   ```bash
   npm start
   ```
4. 브라우저에서 `http://localhost:3000` 접속

