FROM python:3.8.10

ENV PYTHONUNBUFFERED=1
WORKDIR /server

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update && apt-get upgrade -y

#mysql
RUN pip install mysqlclient

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# DB연결되기까지 20초 대기시간 걸어놓기
ENTRYPOINT ["dockerize", "-wait", "tcp://db:3306", "-timeout", "30s"]