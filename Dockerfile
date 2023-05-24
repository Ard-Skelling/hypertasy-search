FROM graphcore/pytorch:3.2.0-ubuntu-20.04-20230314

WORKDIR /usr/src/app

COPY . .

RUN apt update

RUN echo "deb http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse \
    \ndeb http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse \
    \ndeb http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse \
    \ndeb http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse \
    \ndeb http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse \
    \ndeb-src http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse \
    \ndeb-src http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse \
    \ndeb-src http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse \
    \ndeb-src http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse \
    \ndeb-src http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse \
    " > /etc/apt/sources.list && apt update

RUN pip install -r requirements.txt

CMD python main.py