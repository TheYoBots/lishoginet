FROM python:slim

WORKDIR /tmp/lishoginet/
RUN pip install dumb-init && \
    pip install lishoginet

ENTRYPOINT ["dumb-init", "--", "python", "-m", "lishoginet", "--no-conf"]