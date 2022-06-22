# base image
#FROM python:3.6-alpine
FROM python:slim

ENV PYTHONUNBUFFERED 1
# Setting PYTHONUNBUFFERED to a non empty value ensures that the python output is sent straight to terminal

WORKDIR /src

COPY requirements.txt /src/requirements.txt

RUN python -m pip install --upgrade pip
#RUN pip install -r requirements.txt
RUN pip install wheel
RUN pip install uvicorn
RUN pip install "fastapi[all]"

COPY ./code /src/

EXPOSE 8000

# docker-compose will be starting the application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
