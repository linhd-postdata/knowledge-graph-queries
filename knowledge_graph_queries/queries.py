QUERIES = {
    "authors":
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
        '''
}
