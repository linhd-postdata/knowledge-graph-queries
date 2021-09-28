QUERIES = {
    'poeticWorks':
    '''
        PREFIX kos: <http://postdata.linhd.uned.es/kos/>
        PREFIX pdc: <http://postdata.linhd.uned.es/ontology/postdata-core#>
        SELECT ?work ?title ?creator ?date WHERE {

                ?work pdc:title ?title.
                ?work a pdc:PoeticWork.

                ?creation pdc:initiated ?work;
                pdc:hasAgentRole ?ag.
                ?ag pdc:hasAgent ?person;
                    pdc:roleFunction kos:Creator.
                ?person pdc:name ?creator.

                OPTIONAL{
                    ?creation pdc:hasTimeSpan ?sp.
                    ?sp pdc:date ?date.
                }

        } ORDER BY ?title
    ''',

    'poeticWork':
    '''
        PREFIX pdc: <http://postdata.linhd.uned.es/ontology/postdata-core#>
        PREFIX fts: <tag:stardog:api:search:>
        PREFIX kos: <http://postdata.linhd.uned.es/kos/>

        # Construct includes properties that are not in the ontology, but used to put names to the keys
        CONSTRUCT {
            ?work   pdc:score ?score;
                    pdc:name ?resultText;
                    pdc:author ?creator;
                    pdc:date ?date.
        }
        WHERE{
            SELECT ?work ?score ?resultText ?creator ?date WHERE {

                ?work pdc:title ?resultText.
                ?work a pdc:PoeticWork.

                ?creation pdc:initiated ?work;
                pdc:hasAgentRole ?ag.
                ?ag pdc:hasAgent ?person;
                    pdc:roleFunction kos:Creator.
                ?person pdc:name ?creator.

                OPTIONAL{
                    ?creation pdc:hasTimeSpan ?sp.
                    ?sp pdc:date ?date.
                }

                service fts:textMatch {
                    [] fts:query "$*" ;  # Replace $ by query
                        # fts:limit 10;
                        fts:score ?score ;
                        fts:result ?resultText .
                }

            }
        }
        order by desc(?score)
        limit $limit

    ''',
  'authors':
    '''
        PREFIX pdc: <http://postdata.linhd.uned.es/ontology/postdata-core#>
        SELECT DISTINCT ?person ?name ?deathDate ?birthDate
        WHERE{
            ?person a pdc:Person;
                    pdc:name ?name.

            OPTIONAL{
                ?birth pdc:broughtIntoLife ?person;
                pdc:hasTimeSpan ?deathDate.
                ?death pdc:wasDeathOf ?person;
                pdc:hasTimeSpan ?birthDate.
            }
        }
    ''',
    'author':
    '''
        prefix fts: <tag:stardog:api:search:>
        prefix pdc: <http://postdata.linhd.uned.es/ontology/postdata-core#>

        CONSTRUCT {
            ?person pdc:score ?score;
                    pdc:name ?resultText;
                pdc:birthDate ?birthDate;
                pdc:deathDate ?deathDate.
        }

        WHERE{
            SELECT ?person ?score ?resultText ?birthDate ?deathDate WHERE {
            ?person pdc:name ?resultText.
            ?person a pdc:Person.
            service fts:textMatch {
            # Operator * - https://docs.stardog.com/archive/7.5.0/query-stardog/full-text-search.html
                [] fts:query "$*" ;  # Replace $ sign by the query string
                    fts:score ?score ;
                    fts:result ?resultText ;
                    # fts:limit 10 ;
            }
            OPTIONAL{
                  ?birth pdc:broughtIntoLife ?person;
                         pdc:hasTimeSpan ?deathDate.
                  ?death pdc:wasDeathOf ?person;
                         pdc:hasTimeSpan ?birthDate.
            }

            }
        }
        order by desc(?score)
        limit $limit

    ''',


}