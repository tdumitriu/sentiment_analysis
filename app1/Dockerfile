FROM python:3.11-slim

RUN apt-get update && apt-get install --no-install-recommends -y curl

RUN pip install --no-cache-dir pipenv

WORKDIR /usr/speech

RUN pip install setuptools wheel
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY src/ .
COPY bin/start1.sh start1.sh
RUN chmod 755 /usr/speech/start1.sh
RUN mkdir logs

EXPOSE 5018

ENTRYPOINT ["sh", "-c", "/usr/speech/start1.sh"]
