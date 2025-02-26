FROM node:18 as frontend

COPY . .
WORKDIR /HSA-frontend

RUN npm install -g @angular/cli
RUN npm install

RUN ./stream.sh staging

FROM python:3.11 AS backend

COPY --from=frontend . .
WORKDIR /HSA-backend
RUN pip3 install -r requirements.txt

# Final server command
STOPSIGNAL SIGINT
CMD python3 manage.py runserver 0.0.0.0:8000
