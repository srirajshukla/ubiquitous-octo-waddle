FROM python:3
WORKDIR /usr/src/app/ui
COPY ./requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]