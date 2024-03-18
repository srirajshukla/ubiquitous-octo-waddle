# Building and Deploying this Application

## Application Stack
- Backend: FastAPI
- Frontend: Streamlit
- OpenAPI Specification: Swagger
- Database: Postgresql
- Container: Docker
- Deploypment: Azure

## Knowledge Stack
- OpenAIEmbeddings - For generating document embedding vectors
- AzureVectorSearch - For storing the embeddings and searching
- GPT-Turbo-3.5
- AzureDocumentIntelligence
- Langchain


## Setup and Deploy

We have used `Dockerfile` to create containers and `docker-compose.yml` containers which can be easily deployed.

```
# Creating a bridge network
docker network create wfhack
```

The images can be individually created and started using these commands - 

```
# Creating a database image
docker run -d --name db --network wfhack -e POSTGRES_PASSWORD=password -v pgdata:/var/lib/postgresql/data -p 5432:5432 --restart unless-stopped postgres:15.1-alpine
```

```
# Creating the streamlit image
docker run --name ui --network wfhack -p 8501:8501 --restart unless-stopped --link db --link api -e API_BASE_PATH="http://api:8000" ui
```

```
# Creating the backend image
docker run -d --name api --network wfhack -p 8000:8000 -e POSTGRES_CONN_STR="postgresql://postgres:password@db:5432/postgres" --restart unless-stopped --env-file=.env --link db api
```

Or they can all be started at once using docker compose.

```
# Start the do
docker compose up --build
```

## Environment Variables 
Since the application uses multiple Azure services, we need to provision those resources and put their keys in environment variable.

A sample environment files is 

```
AZURE_SEARCH_KEY=
OPENAI_EMBEDDING_API_VERSION=2024-02-15-preview
OPENAI_CHAT_API_VERSION=2023-05-15
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
OPENAI_API_VERSION=2024-02-15-preview
USER_USERNAME=
USER_PASSWORD=
AZURE_CLIENT_ID=
AZURE_TENANT_ID=
AZURE_CLIENT_SECRET=
```