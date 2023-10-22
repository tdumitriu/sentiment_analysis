# Sentiment Analysis 

The sentiment analysis is a process of examination of digital text to ascertain whether the emotional context of the message is favorable, unfavorable, or neutral.
This project builds a service that measures the overall sentiment of a text paragraph.

## Introduction

The service computes the sentiment of a given sentence, or the combined sentiment value of a paragraph.
It follows the following procedure:

- Ingest the input paragraph
- Split the paragraph into sentences
- Analyze the sentiment of each sentence
- Combine the individual sentiments into a list
- Calculate an overall sentiment as a combination of per-sentence sentiment analyses.
- Return the result to the caller

The sentiment analysis returns a "positive", "negative" or "neutral" decision, and a probability from 0 to 1 for each one. The "neutral" one represents the middle range of the [-1.0, +1.0] interval, currently set to [-0.1, +0.1]. The "neutral" decision is an augmentation of the classical bipolar decision. 

## Architecture

The service consists of two servers:
- Server 1:
  - Receives a paragraph of text
  - Splits it into sentences
  - Requests the sentiment analysis for each sentence from the ML server (Server 2)
  - Computes the aggregate sentiment using the "Average Score" aggregation method
  - Simulates a gateway to call the ML server (Server 2) to retrieve the sentiment of a sentence.
- Server 2 (ML server):
  - Computes the sentiment of a given sentence. 
  - This functionality is used by Server 1 and is available via a public endpoint.

## API

### 1. Get a sentiment of a sentence

#### POST /sentiment
Header: `Content-Type: text/html`

Body: `text`

CURL format: `curl -X POST -H "Content-Type: text/html" --data "<sentence>" <hostname>:<port>/sentiment`

### 2. Get a list of sentiments of all sentences in a paragraph
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

### Get an overall sentiment of a paragraph
Header: `Content-Type: application/json`

Body: `json`

CURL format: `curl -X POST -H "Content-Type: application/json" --data-binary "@<filename>" <hostname>:<port>/process`
where the `filename` is the absolute filename (path + file name)

## Build

### Build docker images

The docker images can be built using one of the following methods:
- `docker` command
- `docker-compose` command

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
python src/app2.py
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
- manually - using the `docker run` command
- automatically - using the convenient `docker-compose` tool

#### Run the container using docker

Make sure that there is a docker network called `speech_default` already created.
Check with:
```shell
docker network ls
```
If the network was created you should see something similar to this output:
```shell
df05eb904e2a   speech_default   bridge    local
```
If using `docker-compose`, the network is created automatically. However, it is a good practice to verify the existence of the network.

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
This command builds and brings up the containers.

## Test

Verify that the containers are up and running by executing:
```shell
docker ps
```

The result should show both containers ready for work, like this:
```shell
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS        PORTS                                       NAMES
6dea6f657afe   docker-server1:latest   "sh -c /usr/speech/s…"   13 hours ago   Up 13 hours   0.0.0.0:5018->5018/tcp, :::5018->5018/tcp   server1
3acc64a2219c   docker-server2:latest   "sh -c /usr/speech/s…"   13 hours ago   Up 13 hours   0.0.0.0:5019->5019/tcp, :::5019->5019/tcp   server2
```

Using curl or any other equivalent tool send the following REST commands: 

1. Send the request to the ML server (Server 2) to retrieve the sentiment analysis for a given sentence. This is an internal call.
```shell
curl -X POST -H "Content-Type: text/html" --data "In another moment down went Alice after it, never once considering how in the world she was to get out again." 127.0.0.1:5019/sentiment
```

2. Send the request to Server 1 that acts as a gateway to retrieve the sentiment analysis for a given sentence from the ML server (Server 2).
```shell
curl -X POST -H "Content-Type: text/html" --data "In another moment down went Alice after it, never once considering how in the world she was to get out again." 127.0.0.0:5018/sentiment
```

3. Get the aggregate sentiment analysis for paragraph sent as a json object.
```shell
curl -X POST -H "Content-Type: application/json" --data '{"id":"abc001","text":"Down, down, down. There was nothing else to do, so Alice soon began talking again."}' 127.0.0.1:5018/process
```

4. Get the aggregate sentiment analysis for paragraph sent as binary data.
```shell
curl -X POST -H "Content-Type: text/html" --data-binary "@app1/tests/text1.txt" 127.0.0.1:5018/process
``` 
Note: The `app1/tests/text1.txt` file provided for testing purposes.
