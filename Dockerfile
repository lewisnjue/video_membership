FROM python:3.11

WORKDIR /video_membership

COPY requirements.txt .

RUN python3 -m venv /opt/env && \
    /opt/env/bin/pip install --upgrade pip && \
    /opt/env/bin/pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["/opt/env/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

