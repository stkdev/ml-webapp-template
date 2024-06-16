FROM python:3.11

WORKDIR /app

COPY ./requirements.txt.lock /app/requirements.txt.lock

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt.lock

COPY ./src /app/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

