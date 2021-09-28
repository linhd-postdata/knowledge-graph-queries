#!/usr/bin/python
import stardog
from flask import g
from urllib.parse import unquote
import json

from knowledge_graph_queries.queries import QUERIES


def get_poeticWorks():
    """ Method corresponding to the poeticWorks endpoint

    :return: JSON with the list of all poeticWorks in the knowledge graph
    """
    conn = get_db()
    query = QUERIES['poeticWorks']
    results = conn.select(query, content_type=stardog.content_types.SPARQL_JSON)
    return results


def get_poeticWork(title, limit=10):
    """ Method corresponding to the PoeticWork endpoint

    :param: title: title of poeticWork to retrieve, limit: max number of retrieved elements
    :type: title: str, limit: int
    :return: JSON with the list of poeticWorks with matching title in the knowledge graph
    """
    title = unquote(title)
    conn = get_db()
    query = QUERIES['poeticWork'].replace('$*', title + '*').replace('$limit', str(limit))
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    return process_jsonld(results)


def get_authors():
    """ Method corresponding to the authors endpoint

    :return: JSON with the list of all authors in the knowledge graph
    """
    conn = get_db()
    query = QUERIES['authors']
    results = conn.select(query, content_type=stardog.content_types.SPARQL_JSON)
    return results


def get_author(name, limit=10):
    """ Method corresponding to the author endpoint

    :param: name: name of the author, limit: max number of retrieved elements
    :type: name: str, limit: int
    :return: JSON with the list of all authors with matching names in the knowledge graph
    """
    name = unquote(name)
    conn = get_db()
    query = QUERIES['author'].replace('$*', name + '*').replace('$limit', str(limit))
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    return process_jsonld(results)


def get_manifestations():
    """ Method corresponding to the manifestations endpoint

    :return: JSON with the list of manifestations in the knowledge graph
    """
    # conn = get_db()
    # query = QUERIES['manifestations']
    # results = conn.select(query, content_type=stardog.content_types.SPARQL_JSON)
    # return results
    return {'TODO': 'TODO'}


def get_book(title, limit):
    """ Method corresponding to the book endpoint

    :param: title: title of the book, limit: max number of retrieved elements
    :type: name: str, limit: int
    :return: JSON with the list of all books with matching titles in the knowledge graph
    """
    # title = unquote(title)
    # conn = get_db()
    # query = QUERIES['author'].replace('$*', title + '*').replace('$limit', str(limit))
    # results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    # return process_jsonld(results)
    return {'TODO': '?'}


def connect_to_database():
    connection_details = {
        'endpoint': 'http://62.204.199.252:5820',
        'username': 'admin',
        'password': 'LuckyLuke99',
    }
    database_name = "PD_KG"
    with stardog.Admin(**connection_details) as admin:
        if database_name in [db.name for db in admin.databases()]:
            return stardog.Connection(database_name, **connection_details)
        else:
            raise Exception(f"No database with the name: {database_name}")


def get_db():
    if 'db' not in g:
        g.db = connect_to_database()
    return g.db


def process_jsonld(results):
    results = results.decode('utf8').replace("'", '"')
    return json.loads(results)
