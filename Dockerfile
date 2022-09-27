FROM python:3.10.6-slim-bullseye

ENV HOME /app

WORKDIR $HOME

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

EXPOSE 80

COPY ./training_pipeline /app/training_pipeline

ENTRYPOINT [ "uvicorn", "training_pipeline.serving.app.main:app" ]

CMD [ "--host", "0.0.0.0", "--port", "80" ]
