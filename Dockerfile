FROM python:3.9-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt requirements.txt
RUN /opt/venv/bin/pip install -r requirements.txt

COPY main.service.py .
COPY service/ service/
COPY common/ common/

CMD [ "/opt/venv/bin/python", "main.service.py" ]
