# 기술스택
* Python
* Flask

# 프로세스
### 로그인 request요청시
1. 로그인
2. DB의 user데이터와 비교
3. user데이터와 일치한다면 jwt토큰을 발급
4. response시 토큰을 담아 함께 리턴

### 인증이 필요한 api request 요청시
1. 쿠키에 jwt를 담아 함께 보냄
2. 서버에서 해당 쿠키에 담긴 토큰이 올바른 토큰인지 확인
3. 올바른 토큰이라면 api요청을 수행
