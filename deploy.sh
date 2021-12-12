docker stop job-runner
docker stop logstash-service-job-runner

git pull origin master

docker-compose up --build -d job-runner logstash-service-job-runner
