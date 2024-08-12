# Blind SQL 인젝션 공격 시나리오

## 사용 언어 및 도구

- ![Python](https://img.shields.io/badge/python-3.8%2B-blue)
- ![JavaScript](https://img.shields.io/badge/javascript-ES6%2B-yellow)
- ![jadx](https://img.shields.io/badge/jadx-v1.5-blue)
- ![Frida](https://img.shields.io/badge/frida-15.1.16-green)


### 1. JWT 토큰 탈취

  - Burp Suite를 사용하여 Cross Site Scripting(XSS) JWT 탈취 게시물 작성
![image](https://github.com/user-attachments/assets/e01742f5-1212-4843-b5a6-2824940f42ad)

  
### 2. 토큰 가로채기 서버
- Jadx로 JWT 로그인 함수 확인 후 Snippet
  
![image](https://github.com/user-attachments/assets/d0796cde-83b2-4376-b134-45ad8549087e)
- 탈취한 토큰을 수신

![photo2](https://github.com/user-attachments/assets/88e8947d-c3ba-4d3c-b1a8-f92c1b1cda91)

### 3. Frida를 이용한 앱 조작
- Frida를 사용하여 Android 앱의 WebAppInterface.getToken() 메소드 후킹
- 탈취한 JWT 토큰 사용자로 로그인

![hooking](https://github.com/user-attachments/assets/1068eae3-00fa-4648-9c36-f9f4c69fd756)

### 4. 데이터베이스 추출
- injection.py를 사용하여 블라인드 SQL 인젝션 수행
- 데이터베이스에서 계좌번호와 MD5 해시된 계좌 비밀번호 추출

  ![blind](https://github.com/user-attachments/assets/b829e596-799b-4e0b-8bb9-c1404c7aee0a)

### 5. 무단 자금 이체
- transfer.py를 사용하여 무단 자금 이체 자동화
- 스크립트가 무명증권 앱 UI와 상호작용하여 거래 수행

  ![image](https://github.com/user-attachments/assets/7a6c34c5-cbd8-4370-a914-710573dfeb1e)

  
