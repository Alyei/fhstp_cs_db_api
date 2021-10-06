FROM python:3.10.0-bullseye

ADD . /app
WORKDIR ./app

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0", "app:app"]