FROM python:3.10-slim
WORKDIR /app
COPY . .

RUN chmod +x wait-for-it.sh

EXPOSE 5000

RUN pip3 install -r requirements.txt
