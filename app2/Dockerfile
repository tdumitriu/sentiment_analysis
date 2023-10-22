FROM python:3.11-slim

RUN apt-get update && apt-get install --no-install-recommends -y curl

RUN pip install --no-cache-dir pipenv

WORKDIR /usr/speech

COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install tensorflow
RUN pip install transformers

ENV PYTHONUNBUFFERED 1

COPY src/ .
COPY bin/start2.sh start2.sh
RUN chmod 755 /usr/speech/start2.sh
RUN mkdir logs

EXPOSE 5019

ENTRYPOINT ["sh", "-c", "/usr/speech/start2.sh"]
