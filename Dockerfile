FROM python:slim
COPY . .

RUN pip install requests && \
    pip install lishoginet