
### 초기 설정

```shell
server % docker-compose up --build
```

docker-compose up -d

---

docker build .
docker-compose build
docker-compose up

---

settings.py가 바뀌면 `docker-compose up --build` 필요

---

# 구현 API

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

```mysql
mysql -u root -p

USE test;

SHOW tables;

SELECT * FROM class_course;

INSERT INTO class_course (course_id, name, professor_id)
    -> VALUES ('C001', 'Mathematics', 123),
    ->        ('C002', 'Physics', 456),
    ->        ('C003', 'Chemistry', 789);
Query OK, 3 rows affected (0.06 sec)

mysql> INSERT INTO class_studentcourse (student_id, course_id_id)
    -> VALUES (1, (SELECT id FROM class_course WHERE course_id = 'C001')),
    -> (1, (SELECT id FROM class_course WHERE course_id = 'C002')),
    -> (2, (SELECT id FROM class_course WHERE course_id = 'C001')),
    -> (3, (SELECT id FROM class_course WHERE course_id = 'C003'));
Query OK, 4 rows affected (0.04 sec)
Records: 4  Duplicates: 0  Warnings: 0
```

---

### app name 바꾸었을 때 table 이름 변경 처리

```mysql
mysql> alter table class_course rename to classfile_course;
mysql> alter table class_studentcourse rename to classfile_studentcourse;
```

---

```shell
+--------------------------------+
| Tables_in_test                 |
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
| class_course                   |
| class_studentcourse            |
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
