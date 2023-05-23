FROM python:3.11-buster

WORKDIR /usr/src/woowoo_app

ADD ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY . /usr/src/woowoo_app/

CMD python -m uvicorn main:app --host 0.0.0.0 --port 8089 --workers 4
