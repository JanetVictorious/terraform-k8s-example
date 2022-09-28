FROM python:3.10.6-slim-bullseye

ENV HOME /app

WORKDIR $HOME

COPY requirements.txt .

# Dependencies for building the image using Docker daemon on minikube
ARG BUILD_DEPS="--trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org"

RUN pip install --upgrade pip ${BUILD_DEPS} && \
    pip install -r requirements.txt ${BUILD_DEPS} && \
    rm requirements.txt

EXPOSE 80

COPY ./training_pipeline ./training_pipeline

ENTRYPOINT [ "uvicorn", "training_pipeline.serving.app.main:app" ]

CMD [ "--host", "0.0.0.0", "--port", "80" ]
