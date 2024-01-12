FROM python:3.9-slim

WORKDIR /code/app

COPY ./requirements.txt /code/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

COPY . /code/app

CMD ["python","main.py"]