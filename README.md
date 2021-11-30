# POSTDATA knowlege-graph-queries
Software for embedding the SPARQL queries to POSTDATA knowledge graph and parse the response from Stardog.

A playground interface documenting the API can be found at the `/ui` endpoint.

## Deployment

### Prerequisites

The download of [POSTDATA's triplestore](https://github.com/linhd-postdata/postdata-stardog) is needed.

```bash
$ cd postdata
$ git clone https://github.com/linhd-postdata/postdata-stardog.git
$ git clone https://github.com/linhd-postdata/knowledge-graph-queries.git
$ mv knowledge-graph-queries/docker-compose.yml ./
```

Project structure: 
```
.
├── docker-compose.yml
├── knowledge-graph-queries
│   ├── Dockerfile
│   ├── requirements.txt
│   └── knowledge_graph_queries
│       └── app.py
│           ...
└── postdata-stardog
    ├── stardog
    │   └── config.sh
    │       ...
    └── Dockerfile
```

The compose file defines an application with three services: triplestore and swagger. When deploying the application, docker-compose maps port 5005 of the proxy service container to port 5005 of the host as specified in the file. Make sure port 5005 on the host is not already being in use.

### Deploy with docker-compose

```
$ docker-compose up -d
Creating network "tmp_default" with the default driver
Creating volume "tmp_stardog" with default driver
Creating tmp_triplestore_1 ... done
Creating tmp_swagger_1     ... done
```

### Expected result

Listing containers must show two containers running and the port mapping as below:
```
$ docker ps
CONTAINER ID   IMAGE                                          COMMAND                   CREATED         STATUS         PORTS                                       NAMES
2262f0975e73   linhdpostdata/knowledge-graph-queries:latest   "/bin/sh -c 'sh -c \"…"   9 minutes ago   Up 8 minutes   0.0.0.0:5005->5005/tcp, :::5005->5005/tcp   tmp_swagger_1
f674b87bc2d6   linhdpostdata/postdata-stardog:latest          "/bin/sh -c 'rm -f $…"    9 minutes ago   Up 9 minutes   0.0.0.0:5820->5820/tcp, :::5820->5820/tcp   tmp_triplestore_1
```
After the application starts, navigate to `http://localhost:5005/ui` in your web browser.

### Stop and remove the containers
```
$ docker-compose down
```

## Development

For development, you need to install the package in development mode, and then run `connexion run` command. Alternatively, you could also install the `requirements.txt`.
```bash
$ pip install -e .
$ connexion run knowledge_graph_queries/openapi.yml
```

## Tests

To execute the battery tests, you need to install the package in development mode and the snapshottest package
```bash
$ pip install -e .
$ python setup.py test
```