# knowlege-graph-queries
Software for embedding the SPARQL queries to POSTDATA knowledge graph and parse the response from Stardog.

A playground interface documenting the API can be found at the `/ui` endpoint.

## Deployment
Since `connexion` builds a Flask application from our OpenAPI specification, you can use any WSGI compliant application server. We have tested both `gunicorn` and `uwsgi` and both work fine.
```bash
$ pip install -e .
$ gunicorn knowledge_graph_queries.app:app
```
Alternatively, you can also use the Docker file provided, which exposes the server at the port 5000.
```bash
docker build --tag linhdpostdata/knowledge-graph-queries .
```
Stable versions will be published in the Docker Hub under the `linhdpostdata/poetrylab-api` name.
```bash
$ docker run -p "5000:5000" linhdpostdata/knowledge-graph-queries
```

## Development

For development, you need to install the package in development mode, and then run `connecion run` command. Alternatively, you could also install the `requirements.txt`.
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