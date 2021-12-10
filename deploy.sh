docker stop job-runner

git pull origin master

docker-compose up --build -d job-runner
