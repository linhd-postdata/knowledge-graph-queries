FROM python:3.7.0
ENV WORKERS 4
ENV TIMEOUT 300
ENV PORT 5000
RUN apt-get update -y
RUN apt-get install g++ gfortran libstdc++ -y
RUN pip install -U pip
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install Cython
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn
COPY knowledge_graph_queries ./knowledge_graph_queries
EXPOSE $PORT
CMD sh -c "gunicorn -b 0.0.0.0:${PORT} --workers ${WORKERS} --timeout ${TIMEOUT} knowledge_graph_queries.app:app"