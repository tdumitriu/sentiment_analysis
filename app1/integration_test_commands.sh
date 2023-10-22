docker build -t docker-server1:latest app1
docker build -t docker-server2:latest app2

docker run -ti -p 5018:5018 --network=speech_default --name server1 docker-server1:latest
docker run -ti -p 5019:5019 --network=speech_default --name server2 docker-server2:latest

docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml stop

#APP1
curl 127.0.0.1:5018/
curl 127.0.0.1:5018/status
curl -X POST -H "Content-Type: text/html" --data "In another moment down went Alice after it, never once considering how in the world she was to get out again." 127.0.0.0:5018/sentiment
curl -X POST -H "Content-Type: application/json" --data '{"id":"abc001","text":"Down, down, down. There was nothing else to do, so Alice soon began talking again."}' 127.0.0.1:5018/process
curl -X POST -H "Content-Type: text/html" --data-binary "@app1/tests/text1.txt" 127.0.0.1:5018/process

#APP2
curl 127.0.0.1:5019/
curl 127.0.0.1:5019/status
curl -X POST -H "Content-Type: text/html" --data "In another moment down went Alice after it, never once considering how in the world she was to get out again." 127.0.0.0:5019/sentiment
