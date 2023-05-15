
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
