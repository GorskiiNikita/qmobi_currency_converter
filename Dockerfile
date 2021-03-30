# pull official base image
FROM python:3.8.3-alpine

# copy project
COPY utils.py utils.py
COPY data_loader.py data_loader.py
COPY server.py server.py

CMD [ "python3", "server.py" ]