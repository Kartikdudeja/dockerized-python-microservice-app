# base image
#FROM python:3.6-alpine
FROM python:slim

# Setting PYTHONUNBUFFERED to a non empty value ensures that the python output is sent straight to terminal
ENV PYTHONUNBUFFERED 1

WORKDIR /src

RUN apt-get update && apt-get -y install libpq-dev gcc
RUN python -m pip install --upgrade pip

#COPY ./code/requirements.txt /src/
COPY ./pyapp/code/requirements.txt /src
RUN pip install -r requirements.txt

#COPY ./code /src/
COPY ./pyapp/code /src

EXPOSE 8000

# docker-compose will be starting the applicationps
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]