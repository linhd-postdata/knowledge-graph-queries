FROM python:3.9
ENV WORKERS 4
ENV TIMEOUT 300
ENV PORT 5005
RUN apt update -y &&\
    apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools &&\
    pip install -U pip
WORKDIR /usr/src/app
COPY requirements.txt setup.py setup.cfg ./
# RUN pip install Cython
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir gunicorn
COPY knowledge_graph_queries ./knowledge_graph_queries
RUN pip install -e .
EXPOSE $PORT
# CMD sh -c "gunicorn -b 0.0.0.0:${PORT} --workers ${WORKERS} --timeout ${TIMEOUT} knowledge_graph_queries.app:app"
CMD sh -c "connexion run -p ${PORT} knowledge_graph_queries/openapi/openapi.yml"
