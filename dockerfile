FROM nikolaik/python-nodejs:python3.9-nodejs12-slim

WORKDIR /app
COPY frontend/app/package*.json ./
COPY backend/requirements.txt ./
RUN npm install && pip install -r requirements.txt
RUN apt-get update && apt-get install redis -y

COPY frontend/app /app/frontend/app
WORKDIR /app/frontend/app
RUN npm run build


ADD . /app
WORKDIR /app


CMD ./detach_app.sh