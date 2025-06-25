FROM python:3-slim

COPY requirements.txt /
COPY extract_stream_url.py /
COPY docker_run.sh /

RUN pip install -r requirements.txt
RUN mkdir /out

CMD [ "sh", "-c", "/docker_run.sh" ]
