FROM python:latest

WORKDIR /video_membership

COPY . /video_membership

RUN python3 -m venv /opt/env

RUN  pip install /opt/env/bin/pip --upgrade

RUN  /opt/env/pip install -r requirements.txt


CMD /opt/env/bin/uvicorn app.main:app 