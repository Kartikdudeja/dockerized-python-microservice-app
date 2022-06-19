# base image
FROM python:3.9

WORKDIR /src

# dependencies
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./code /src/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
