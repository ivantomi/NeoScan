FROM python:3.8-slim

WORKDIR /app

COPY *requirements.txt /app/

RUN apt-get update && apt-get install git -y &&\
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

RUN pip install -e .

EXPOSE 8080
CMD ["gunicorn", "-b", ":8080", "--workers=1", "src.app:app", "--reload"]

