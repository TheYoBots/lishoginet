FROM python:slim

LABEL maintainer "Manuel Klemenz <manuel.klemenz@gmail.com>"

WORKDIR /tmp/lishoginet/
RUN pip install dumb-init && \
    pip install lishoginet

ENTRYPOINT ["dumb-init", "--", "python", "-m", "lishoginet", "--no-conf"]