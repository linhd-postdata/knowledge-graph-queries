#!/usr/bin/python
import stardog
from flask import g, current_app
from urllib.parse import unquote
import json
from pyld import jsonld
from knowledge_graph_queries.queries import QUERIES, CONTEXT


def get_poeticWorks():
    """ Method corresponding to the poeticWorks endpoint

    :return: JSON with the list of all poeticWorks in the knowledge graph
    """
    conn = get_db()
    query = QUERIES['poeticWorks']
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    jsonld_results = json.loads(results)
    compacted = jsonld.compact(jsonld_results, CONTEXT)
    graph = compacted.get("@graph")
    return graph


def get_poeticWork(title, limit=10):
    """ Method corresponding to the PoeticWork endpoint

    :param title: title of poeticWork to retrieve
    :type title: str
    :param limit: max number of retrieved elements
    :type limit: int
    :return: JSON with the list of poeticWorks with matching title in the knowledge graph
    """
    title = unquote(title)
    conn = get_db()
    query = QUERIES['poeticWork'].replace('$*', title + '*').replace('$limit', str(limit))
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    jsonld_results = json.loads(results)
    compacted = jsonld.compact(jsonld_results, CONTEXT)
    # return process_jsonld(results)
    graph = compacted.get("@graph")
    return graph


def get_authors():
    """ Method corresponding to the authors endpoint

    :return: JSON with the list of all authors in the knowledge graph
    """
    conn = get_db()
    query = QUERIES['authors']
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    jsonld_results = json.loads(results)
    compacted = jsonld.compact(jsonld_results, CONTEXT)
    graph = compacted.get("@graph")
    return graph


def get_author(name, limit=10):
    """ Method corresponding to the author endpoint

    :param name: name of the author,
    :type name: str
    :param limit: max number of retrieved elements
    :type  limit: int
    :return JSON with the list of all authors with matching names in the knowledge graph
    """
    name = unquote(name)
    conn = get_db()
    query = QUERIES['author'].replace('$*', name + '*').replace('$limit', str(limit))
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    jsonld_results = json.loads(results)
    compacted = jsonld.compact(jsonld_results, CONTEXT)
    # return process_jsonld(results)
    graph = compacted.get("@graph")
    return graph


def get_author_profile(uri):
    """Method to fetch data related to a given author

    :param uri: the URI of the author resource
    :type uri: str
    :return JSON with personal information and associated poetic works
    """
    query = QUERIES['author_profile'].replace('$', uri)
    conn = get_db()
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    json_ld_result = json.loads(results)
    framed = jsonld.frame(json_ld_result,
        {
            "http://postdata.linhd.uned.es/ontology/postdata-core#works": {
                "@embed": "@always"
            }
        }
    )
    compacted = jsonld.compact(framed, CONTEXT)
    # print(json.dumps(compacted, indent=2))
    del compacted["@context"]
    return compacted


def get_redactions(uri):
    """Method to return all the redactions or editions of a particular poetic
    work

    :param uri: the URI of the poetic work resource
    :type uri: str
    :return JSON with redaction related information including contributor
    information, textual content and physical editions
    """
    query = QUERIES['redactions'].replace('$', uri)
    print(query)
    conn = get_db()
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    json_ld_result = json.loads(results)
    print(json.dumps(json_ld_result, indent=2))
    framed = jsonld.frame(json_ld_result, {
        "http://postdata.linhd.uned.es/ontology/postdata-core#isRealisedThrough" : {
            "@embed": "@always"
        }
    })
    compacted = jsonld.compact(framed, CONTEXT)
    del compacted["@context"]
    return compacted


def get_scansion(uri):
    """Method to return the basic structure of a particular scansion

    :param uri: the URI of the scansion resource
    :type uri: str
    :return JSON with scansion information including lists of structural units
    (stanzas, lines, words, punctuations) and analytical units (grammatical and
    metrical syllables, feet and morae), metrical information (redaction,
    stanza and line patterns), and literary device annotations (enjambment,
    shceme, tropes, intertextuality, etc.)
    """
    query = QUERIES['scansion_structure'].replace('$', uri)
    print(query)
    conn = get_db()
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    json_ld_result = json.loads(results)
    # print(json.dumps(json_ld_result, indent=2))
    framed = jsonld.frame(json_ld_result, {
        "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#stanzaList":{
            "@embed": "@always",
            "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#lineList":{
                    "@embed": "@always",
                "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasMetricalSyllable":{
                    "@embed": "@always",
                },
                "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasGrammaticalSyllable":{
                    "@embed": "@always",
                    "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isGrammaticalSyllableAnalysedBy":{
                        "@embed": "@never"
                    }
                },
                "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasWord":{
                    "@embed": "@always",
                    "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isWordAnalysedBy":{
                        "@embed": "@never"
                    }
                },
            },
        },
        "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#metaplasm":{
            "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#affectsFirstWord":{
                "@embed": "@never"
            }
        },
        "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#enjambment":{
            "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#affectsLine":{
                "@embed": "@never"
            }
        }
    })
    print(json.dumps(framed, indent=2))
    compacted = jsonld.compact(framed, CONTEXT)
    # graph = compacted.get("@graph")
    del compacted["@context"]
    with open('jsonld.json', 'w') as f:
        json.dump(compacted, f)
    return compacted


def get_scansion_file(id):
    """Method to return all the information about a scansion.
    It returns the file from the document store.

    :param id: the ID of the file (name) in the document store.
    :return JSON with information about a scansion"""
    conn = get_db()
    doc_store = conn.docs()
    retrieved_file = doc_store.get(id)
    return retrieved_file


def get_scansion_line(uri):
    """Method to return detailed information for a scanned line

    :param uri: the URI of the line resource
    :type uri: str
    :return JSON with scansion information related to the line including
    punctuation, words, metrical syllables, grammatical syllables, morae and
    feet whenever applicable
    """
    query = QUERIES['scansion_line'].replace('$', uri)
    conn = get_db()
    results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    json_ld_result = json.loads(results)
    print(json.dumps(json_ld_result, indent=2))
    framed = jsonld.frame(json_ld_result, {
        "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasGrammaticalSyllable": {
        },
        "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasMetricalSyllable":{
        },
        "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasWord":{
        },
        "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasPunctuation":{
        },
    })
    compacted = jsonld.compact(framed, CONTEXT)
    return compacted


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

    :param title: title of the book
    :type title: str
    :param limit: max number of retrieved elements
    :type limit: int
    :return JSON with the list of all books with matching titles in the knowledge graph
    """
    # title = unquote(title)
    # conn = get_db()
    # query = QUERIES['author'].replace('$*', title + '*').replace('$limit', str(limit))
    # results = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    # return process_jsonld(results)
    return {'TODO': '?'}


def connect_to_database(host="http://triplestore", port=5820):
    """ Establish connection with knowledge graph

    :param host: name of the service in docker-compose.yml
    :type host: str
    :param port: port for Stardog instance
    :type port: int
    :return: stardog.Connection with knowledge graph
    """
    connection_details = {
        'endpoint': f"{host}:{port}",
        'username': 'admin',
        'password': 'LuckyLuke99'
    }
    # database_name = "PD_KG_SPA"
    database_name = "PD_KG"
    with stardog.Admin(**connection_details) as admin:
        if database_name in [db.name for db in admin.databases()]:
            return stardog.Connection(database_name, **connection_details)
        else:
            raise Exception(f"No database with the name: {database_name}")


def get_db():
    """ Checks if the connection in the application context (request) is established,
    if yes returns existing connection, if not creates a new connection and returns it

    :return: existing or new stardog.Connection with knowledge graph
    """
    if 'db' not in g:
        g.db = connect_to_database()
    return g.db


def process_jsonld(results):
    """ decode bytes-like objet into valid JSON format

    :return: data in valid JSON format
    """
    results = results.decode('utf8').replace("'", '"')
    return json.loads(results)
