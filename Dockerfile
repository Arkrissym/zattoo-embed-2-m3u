FROM python:3-slim

COPY requirements.txt /
COPY app.py /
COPY docker_run.sh /

RUN pip --no-cache-dir install -r requirements.txt
RUN rm requirements.txt

RUN mkdir /out
RUN chmod +x /docker_run.sh

ENTRYPOINT [ "/docker_run.sh" ]
