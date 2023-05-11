FROM graphcore/pytorch:3.2.0-ubuntu-20.04-20230314

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python main.py