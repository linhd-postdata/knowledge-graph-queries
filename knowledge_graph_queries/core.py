#!/usr/bin/python
import stardog
from flask import g, current_app
from urllib.parse import unquote
import json
from pyld import jsonld
from knowledge_graph_queries.queries import QUERIES, CONTEXT, CONTEXT_QUERY
from SPARQLWrapper import SPARQLWrapper, JSONLD


def send_query(query, sparql):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSONLD)
    try:
        result = sparql.queryAndConvert().serialize(format='json-ld', indent=4)
        result = json.loads(result)
    except Exception as e:
        print('error')
        result = [f'output error: {e}']
    return result if result else 'none'


def get_authors():
    """ Method corresponding to the poeticWorks endpoint

    :return: JSON with the list of all poeticWorks in the knowledge graph
    """
    query = QUERIES['authors']
    sparql = connect_to_database()
    result = send_query(query, sparql)
    result = jsonld.compact(result, CONTEXT)
    result = result.get("@graph")
    return result




def get_poeticWorks():
    """ Method corresponding to the poeticWorks endpoint

    :return: JSON with the list of all poeticWorks in the knowledge graph
    """
    query = QUERIES['poeticWorks']
    sparql = connect_to_database()
    result = send_query(query, sparql)
    result = jsonld.compact(result, CONTEXT)
    result = result.get("@graph")
    return result


def get_poeticWork(title, limit=10):
    """ Method corresponding to the PoeticWork endpoint

    :param title: title of poeticWork to retrieve
    :type title: str
    :param limit: max number of retrieved elements
    :type limit: int
    :return: JSON with the list of poeticWorks with matching title in the knowledge graph
    """
    query = QUERIES['poeticWork']
    if (name_len:=len(title)) < 4:
        query = query.replace("$*", title).replace("$limit", str(limit))
    else:
        query = query.replace("$*", f"{title}*").replace("$limit", str(limit))
    sparql = connect_to_database()
    result = send_query(query, sparql)
    result = jsonld.compact(result, CONTEXT)
    del result["@context"]
    return result


def get_authors_old():
    """ Method corresponding to the authors endpoint

    :return: JSON with the list of all authors in the knowledge graph
    """
    conn = get_db()
    query = QUERIES['authors']
    result = conn.graph(query, content_type=stardog.content_types.LD_JSON)
    compacted = jsonld.compact(result, CONTEXT)
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
    query = QUERIES['author']
    if (name_len:=len(name)) < 4:
        query = query.replace("$*", name).replace("$limit", str(limit))
    else:
        query = query.replace("$*", f"{name}*").replace("$limit", str(limit))
    sparql = connect_to_database()
    result = send_query(query, sparql)
    compacted = jsonld.compact(result, CONTEXT)
    # return process_jsonld(results)
    del compacted["@context"]
    return compacted


def get_author_profile(uri):
    """Method to fetch data related to a given author

    :param uri: the URI of the author resource
    :type uri: str
    :return JSON with personal information and associated poetic works
    """
    query = QUERIES['author_profile'].replace('$', uri)
    sparql = connect_to_database()
    
    result = send_query(query, sparql)
    framed = jsonld.frame(result,
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
    query = QUERIES['redactions'].replace('$', uri)
    sparql = connect_to_database()
    
    result = send_query(query, sparql)
    framed = jsonld.frame(result, {
        "http://postdata.linhd.uned.es/ontology/postdata-core#isRealisedThrough" : {
            "@embed": "@always"
        }
    })
    compacted = jsonld.compact(framed, CONTEXT)
    del compacted["@context"]
    return compacted



def get_redactions_old(uri):
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
    query = QUERIES['scansion_query'].replace('$', uri)
    # print(query)
    sparql = connect_to_database()
    
    result = send_query(query, sparql)
    # print(json.dumps(json_ld_result, indent=2))
    framed = jsonld.frame(result, json.loads("""{
    	"http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#stanzaList": {
    		"@embed": "@always",
    		"http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#lineList": {
    			"@embed": "@always"
    		}
    	}
    }"""))
    # print(json.dumps(framed, indent=2))
    compacted = jsonld.compact(framed, CONTEXT_QUERY)
    # graph = compacted.get("@graph")
    del compacted["@context"]
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


def connect_to_database(host="https://poetry.linhd.uned.es", port=5820):
    """ Establish connection with knowledge graph

    :param host: name of the service in docker-compose.yml
    :type host: str
    :param port: port for Stardog instance
    :type port: int
    :return: stardog.Connection with knowledge graph
    """
    connection_details = {
        'endpoint': 'https://poetry.linhd.uned.es/sparql:5820',
    }
    sparql = SPARQLWrapper("http://poetry.linhd.uned.es:5820/sparql")
    sparql.setTimeout(100)
    return sparql


def process_jsonld(results):
    """ decode bytes-like objet into valid JSON format

    :return: data in valid JSON format
    """
    results = results.decode('utf8').replace("'", '"')
    return json.loads(results)
