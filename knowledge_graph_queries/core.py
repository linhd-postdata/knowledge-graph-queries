#!/usr/bin/python
import stardog
from flask import g
from urllib.parse import unquote
import json

from queries import QUERIES


def get_poeticWorks():
    conn = get_db()
    query = QUERIES['poeticWorks']
    results = conn.select(query, content_type=stardog.content_types.SPARQL_JSON)
    return results


def get_poeticWork(title, limit=10):
    title = unquote(title)
    conn = get_db()
    query = QUERIES['poeticWork'].replace('$*', title + '*').replace('$limit', str(limit))
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    return process_jsonld(results)


def get_authors():
    conn = get_db()
    query = QUERIES['authors']
    results = conn.select(query, content_type=stardog.content_types.SPARQL_JSON)
    return results


def get_author(name, limit=10):
    name = unquote(name)
    conn = get_db()
    query = QUERIES['author'].replace('$*', name + '*').replace('$limit', str(limit))
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    return process_jsonld(results)


def get_manifestations():
    # conn = get_db()
    # query = QUERIES['manifestations']
    # results = conn.select(query, content_type=stardog.content_types.SPARQL_JSON)
    # return results
    return {'TODO': 'TODO'}


def get_book(title):
    # title = unquote(title)
    # conn = get_db()
    # query = QUERIES['book']
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
