# code

## Run migrations with
alembic upgrade head

## Start server with
uvicorn endpoints:app --reload

docker network create wfhack

docker compose up --build

docker run -d --name db --network wfhack -e POSTGRES_PASSWORD=password -v pgdata:/var/lib/postgresql/data -p 5432:5432 --restart unless-stopped postgres:15.1-alpine

POSTGRES_CONN_STR="postgres://postgres:password@db:5432/postgres"

docker run --name ui --network wfhack -p 8501:8501 --restart unless-stopped --link db --link api -e API_BASE_PATH="http://api:8000" ui

docker run -d --name api --network wfhack -p 8000:8000 -e POSTGRES_CONN_STR="postgresql://postgres:password@db:5432/postgres" --restart unless-stopped --env-file=.env --link db api

docker run -d --name proxy --network wfhack -p 8080:80 --link api --link ui webserver:latest 
