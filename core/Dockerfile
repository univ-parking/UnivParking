FROM python:3.10

# 컨테이너 내 프로젝트 root directory 설정
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 필요한 module 설치
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 프로젝트 코드 복사
COPY . .

### 이 아래 command들은 docker-compose에 작성할 내용이므로, 확인 후 삭제한다.
# 포트 설정
