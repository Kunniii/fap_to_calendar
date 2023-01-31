FROM python:3.10-alpine
WORKDIR /app
COPY ./src./* /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]