# Sentiment Analysis 

The sentiment analysis is a process of examination of digital text to ascertain whether the emotional context of the message is favorable, unfavorable, or neutral.
This project builds a service that provides a tool that measures the sentiment of a text paragraph.

## Introduction

The process of analyzing and measuring the sentiment of a paragraph follows these steps:

- ingests the input paragraph
- splits the paragraph into sentences
- analyzes the sentiment of each sentence
- combines the individual sentiments into a list
- calculates an overall sentiment as a combination of the per-sentence analysis of all sentences in the paragraph.
- return the result to the caller

The sentiment analysis returns a "positive", "negative" or "neutral" decision, and a probability from 0 to 1 for each one. The "neutral" one represents the "middle" spot of the [-1, +1] interval, currently set to [-0.1, +0.1]. We added the "neutral" decision as an augmentation to the classical set of bipolar decision. 

The service computes the sentiment of a given sentence, or the combined sentiment value of a paragraph.

## API

### 1. Get the sentiment of a sentence

#### POST /sentiment
Header: `Content-Type: text/html`

Body: `text`

CURL format: `curl -X POST -H "Content-Type: text/html" --data "<sentence>" <hostname>:<port>/sentiment`

### Get the combined sentiment of a paragraph (uploading json)
Header: `Content-Type: application/json`

Body: `json`

CURL format: `curl -X POST -H "Content-Type: application/json" --data "<json>" <hostname>:<port>/process`
where the `json` object has the following format:
```json
{ 
  "id": "abc001",
  "text": <paragraph>
}
```

### Get the combined sentiment of a paragraph (uploading binary data)
Header: `Content-Type: application/json`

Body: `json`

CURL format: `curl -X POST -H "Content-Type: application/json" --data-binary "@<filename>" <hostname>:<port>/process`
where the `filename` is the absolute filename (path + file name)

## Build

### Build docker images

The docker images can be built using one of these methods:
- docker command
- docker-compose command

##### Prerequisites
- Make sure that you have the latest docker engine installed.
- Stop and remove any existing container associated with this project.
- Run the commands from the root of the project.

**Using docker**
```dockerfile
docker build -t docker-server1:latest app1
docker build -t docker-server2:latest app2
```
- The docker images for both servers will be created or updated but the containers will NOT be started.
- To start the containers see section **Run**

**Using docker-compose**
- Make sure that you have installed the docker compose plugin or independent module

```dockerfile
docker-compose -f docker-compose.yml up -d
```
- The docker images for both servers will be created or updated and the containers will be started.
 
## Run

### Locally

**Prerequisite**: Make sure that you have the `HOSTNAME_APP2=127.0.0.1` environment variable setup in your local environment.

Start the servers in new terminals (recommended)
```shell
python src/app1.py
```
and
```shell
python src/app1.py
```
From a different terminal (recommended) test that the servers are up and running:
```shell
curl 127.0.0.1:5018/
curl 127.0.0.1:5018/status
```
and
```shell
curl 127.0.0.1:5019/
curl 127.0.0.1:5019/status
```
Note: The server ports are:
 - 5018 - for server1
 - 5019 - for server2

### Containerized

The containers can be started in two ways:
- manually - using the docker run command
- automatically - using the convenient docker-compose tool

#### Run the container using docker

Make sure that there is a docker network called speech_default already created.
Check with:
```shell
docker network ls
```
If the network was created you should see something similar to this output:
```shell
df05eb904e2a   speech_default   bridge    local
```
If the docker-compose was used then the network was automatically created. Regardless, it is a good practice to verify the existence of the network.

Execute the following docker commands to bring the containers up:
```shell
docker run -ti -p 5018:5018 --network=speech_default --name server1 docker-server1:latest
docker run -ti -p 5019:5019 --network=speech_default --name server2 docker-server2:latest
```

#### Run the container using docker-compose
Execute the following command:
```shell
docker-compose -f docker-compose.yml up -d
```
This command should build and bring up the containers.

#### Test

Verify that the containers are up and running by executing:
```shell
docker ps
```

The result should show both containers ready for work:
```shell
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS        PORTS                                       NAMES
6dea6f657afe   docker-server1:latest   "sh -c /usr/speech/s…"   13 hours ago   Up 13 hours   0.0.0.0:5018->5018/tcp, :::5018->5018/tcp   server1
3acc64a2219c   docker-server2:latest   "sh -c /usr/speech/s…"   13 hours ago   Up 13 hours   0.0.0.0:5019->5019/tcp, :::5019->5019/tcp   server2
```

Run the following tests to verify that the servers work as expected:

##### Endpoints

Use curl or any other equivalent tool to send the following REST requests: 

1. Send the request to the second server (ML) to retrieve the sentiment analysis for a given sentence.
```shell
curl -X POST -H "Content-Type: text/html" --data "In another moment down went Alice after it, never once considering how in the world she was to get out again." 127.0.0.1:5019/sentiment
```

2. Send the request to the first server that acts as a gateway, to retrieve the sentiment analysis for a given sentence, serviced by the second server.
```shell
curl -X POST -H "Content-Type: text/html" --data "In another moment down went Alice after it, never once considering how in the world she was to get out again." 127.0.0.0:5018/sentiment
```

3. Get the aggregate sentiment analysis for paragraph sent as a json object.
```shell
curl -X POST -H "Content-Type: application/json" --data '{"id":"abc001","text":"Down, down, down. There was nothing else to do, so Alice soon began talking again."}' 127.0.0.1:5018/process
```

4. Get the aggregate sentiment analysis for paragraph sent as binary.
```shell
curl -X POST -H "Content-Type: text/html" --data-binary "@app1/tests/text1.txt" 127.0.0.1:5018/process
``` 
Note: The `app1/tests/text1.txt` is added for testing purpose.
