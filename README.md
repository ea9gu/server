# 📚 비가청 주파수를 활용한 수업 출석체크 앱, 공책

이화여자대학교 2023 상반기 졸업프로젝트


## 💫 System Architecture

<img width="580" alt="architecture" src="https://github.com/ea9gu/server/assets/69420512/f675ffe0-1b93-47ea-a1ba-abcdca9b46fb">



## 💫 구현 API

### 로그인 & 회원가입 관련

|Method <br> |URL <br> |Description <br> |
|:---:|:---:|:---:|
|`POST`|/user/account/mylogin/|login|
|`POST`|/user/account/view_user_info/|view user information|
|`POST`|/user/account/signup/|회원 가입|
|`POST`|/user/account/password/change/|비밀번호 변경|
|`POST`|/user/account/password/reset/|비밀번호 리셋|


### 주파수 수신 & 발신 & 확인
|Method <br> |URL <br> |Description <br> |
|:---:|:---:|:---:|
|`GET`|/freq/generate-freq/|교수 출석 체크 시 주파수 생성 및 발생|
|`POST`|/freq/save-attendance/|학생 출석 체크 시 주파수 확인 및 출석 체크|


### 기기 등록 
|Method <br> |URL <br> |Description <br> |
|:---:|:---:|:---:|
|`POST`|/serial/save-device/|유효한 기기 등록|


### 수업 정보 
|Method <br> |URL <br> |Description <br> |
|:---:|:---:|:---:|
|`POST`|/class/create-and-enroll/|새로운 수업 등록|
|`POST`|/class/sutdent-course/|특정 학생이 듣는 모든 수업 정보 추출|
|`POST`|/class/prof-course/|특정 교수의 모든 수업 정보 추출|

### 출석 체크
|Method <br> |URL <br> |Description <br> |
|:---:|:---:|:---:|
|`POST`|/class/activate-signal/|수업 출석 체크 버튼 활성화|
|`POST`|/class/fix-attendance/|학생의 출석 체크를 교수가 임의로 변경 시 출석 정보 변경|

---


## 💫 Run in Local

```docker-compose up --build```

.env file 지정 필요

---

### Database Table List

```
+--------------------------------+
| Tables                |
+--------------------------------+
| account_emailaddress           |
| account_emailconfirmation      |
| accounts_user                  |
| accounts_user_groups           |
| accounts_user_user_permissions |
| auth_group                     |
| auth_group_permissions         |
| auth_permission                |
| authtoken_token                |
| classfile_course               |
| classfile_studentcourse        |
| django_admin_log               |
| django_content_type            |
| django_migrations              |
| django_session                 |
| django_site                    |
| freq_attendance                |
| freq_audiofile                 |
| serial_device                  |
| socialaccount_socialaccount    |
| socialaccount_socialapp        |
| socialaccount_socialapp_sites  |
| socialaccount_socialtoken      |
+--------------------------------+
```

### 👋 Team Ea9gu

2022.09 ~ 2023.06

|김주연 <br> |김유민 <br> |장예서 <br> |
|:---:|:---:|:---:|
|Frontend<br>UI/UX|Frontend<br>UI/UX|Backend<br>DevOps|
