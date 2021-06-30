FROM nikolaik/python-nodejs:python3.9-nodejs12-slim

WORKDIR /app
ADD . /app

WORKDIR /app/frontend/app
RUN npm install && npm run build

WORKDIR /app/backend
RUN pip install -r requirements.txt


EXPOSE 3001

CMD python manager.py runserver