FROM graphcore/pytorch:3.2.0-ubuntu-20.04-20230314

WORKDIR /usr/src/app

COPY . .

RUN echo "deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib \
    \ndeb-src https://mirrors.aliyun.com/debian/ bullseye main non-free contrib \
    \ndeb https://mirrors.aliyun.com/debian-security/ bullseye-security main \
    \ndeb-src https://mirrors.aliyun.com/debian-security/ bullseye-security main \
    \ndeb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib \
    \ndeb-src https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib \
    \ndeb https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib \
    \ndeb-src https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib \
    " > /etc/apt/sources.list && apt update

RUN pip install -r requirements.txt

CMD python main.py