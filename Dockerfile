FROM python:alpine3.9
ENV WORKERS 4
ENV TIMEOUT 300
ENV PORT 5000
RUN apk update &&\
    apk upgrade &&\
#     apk add --no-cache g++ gfortran libstdc++ &&\
    pip install -U pip
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn
COPY knowledge_graph_queries ./knowledge_graph_queries
EXPOSE $PORT
CMD sh -c "gunicorn -b 0.0.0.0:${PORT} --workers ${WORKERS} --timeout ${TIMEOUT} knowledge_graph_queries.app:app"
