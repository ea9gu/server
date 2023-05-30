# 비가청 주파수를 활용한 수업 출석체크 앱, 공책

이화여자대학교 2023 상반기 졸업프로젝트


### Local

```docker-compose up --build```


## System Architecture

<img width="580" alt="architecture" src="https://github.com/ea9gu/server/assets/69420512/0d31b4da-f6ca-43bf-a10e-ad937bdd58c0">


## 구현 API

## 로그인 & 회원가입 관련
✔ 로그인: /user/account/login/

✔ 로그아웃: /user/account/password/logout/

✔ 회원가입: /user/account/signup/

✔ 비밀번호 변경: /user/account/password/change/

✔ 비밀번호 리셋: /user/account/password/reset/

## 주파수 주고받기 관련
✔ 교수 앱에서 주파수 생성 요청: /freq/generate-freq/

✔ 학생 앱에서 주파수 확인 및 출석체크 요청: /freq/save-attendance/

## 기기 등록 관련
✔ 기기 등록: /serial/save-device/


## 수업 등록 및 관리 관련
✔ 수업 등록: /class/create-and-enroll/
<!-- ✔ 수업 등록: /class/create-course/

✔ csv 파일로 수강 학생 등록: /class/enroll-students/ -->

## 과목 정보 관련
✔ 특정 학생이 듣는 모든 수업 정보 가져오기: /class/student-course/

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
