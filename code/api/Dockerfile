FROM python:3.12.2
WORKDIR /usr/src/app/api
COPY ./requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip
RUN pip install -r requirements.txt
COPY . . 
EXPOSE 8000
CMD ["bash", "-c", "alembic upgrade head && gunicorn endpoints:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"]