FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./run.py ./run.py
COPY ./peekaboo ./peekaboo

CMD [ "python3", "run.py"]
