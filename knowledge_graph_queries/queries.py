QUERIES = {
    'poeticWorks':
    '''
PREFIX kos: <http://postdata.linhd.uned.es/kos/>
PREFIX pdc: <http://postdata.linhd.uned.es/ontology/postdata-core#>

CONSTRUCT{
    ?work pdc:title ?title;
        pdc:author ?creator;
        pdc:date ?date.
}

WHERE {
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

CONSTRUCT {
    ?person pdc:name ?name;
        pdc:deathDate ?deathDate;
        pdc:birthDate ?birthDate;
        pdc:deathPlace ?deathPlaceLabel;
        pdc:birthPlace  ?birthPlaceLabel.
}
WHERE{
    ?person a pdc:Person;
            pdc:name ?name.

    OPTIONAL{
        ?birth pdc:broughtIntoLife ?person;
        pdc:hasTimeSpan ?birthSpan.
        ?birthSpan pdc:date ?birthDate.
    }

    OPTIONAL{
        ?death pdc:wasDeathOf ?person;
        pdc:hasTimeSpan ?deathSpan.
        ?deathSpan pdc:date ?deathDate.
    }  


    OPTIONAL{
        ?birth pdc:broughtIntoLife ?person;
        pdc:tookPlaceAt ?birthPlace.
        ?birthPlace rdfs:label ?birthPlaceLabel.
    }
    
    OPTIONAL {
        ?death pdc:wasDeathOf ?person;
        pdc:tookPlaceAt ?deathPlace.
        ?deathPlace rdfs:label ?deathPlaceLabel.
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
                pdc:deathDate ?deathDate;
                pdc:deathPlace ?deathPlaceLabel;
                pdc:birthPlace  ?birthPlaceLabel.
                
        }
        
        WHERE {
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
                pdc:hasTimeSpan ?birthSpan.
                ?birthSpan pdc:date ?birthDate.
            }
            OPTIONAL{
                ?death pdc:wasDeathOf ?person;
                pdc:hasTimeSpan ?deathSpan.
                ?deathSpan pdc:date ?deathDate.
            }
            OPTIONAL{
                ?birth pdc:broughtIntoLife ?person;
                pdc:tookPlaceAt ?birthPlace.
                ?birthPlace rdfs:label ?birthPlaceLabel.
            }
            OPTIONAL {
                ?death pdc:wasDeathOf ?person;
                pdc:tookPlaceAt ?deathPlace.
                ?deathPlace rdfs:label ?deathPlaceLabel.
            }
        }
        order by desc(?score)
        limit 10
    ''',
    'author_profile':
    '''
# This query returns a set of information for an author
# Inlucdes personal information
# Organisations the person may belong to
# Poetic works and the number of editions for each work

CONSTRUCT{
    ?author pdc:portrait ?portrait;
        pdc:movement ?movement;
        pdc:name ?name;
        pdc:portrait ?portrait;
        pdc:additionalName ?additionalName;
        pdc:alternativeName ?alternativeName;
        pdc:biography ?biography;
        pdc:forename ?forename;
        pdc:genName ?genName;
        pdc:ethnicity ?ethnicity;
        pdc:gender ?gender;
        pdc:works ?poeticWork;
        pdc:birthDate ?birthDate;
        pdc:deathDate ?deathDate;
        pdc:nationality ?nationality;
        pdc:occupation ?occupation;
        pdc:birthPlace ?birthPlaceLabel;
        pdc:deathPlace ?deathPlaceLabel;
        pdc:religiousAffiliation ?religion.
    
    ?poeticWork  pdc:roleFunction ?role;
        pdc:title ?title;
        pdc:date ?date;
}

WHERE{
    BIND (<$> AS ?author).
    ?author pdc:isAgentOf ?agentRole;
        pdc:name ?name.
    
    ?creation pdc:hasAgentRole ?agentRole;
        pdc:initiated ?poeticWork;
        a pdc:WorkConception.
    
    ?agentRole pdc:roleFunction ?role;
        pdc:hasAgent ?author.
    
    ?poeticWork pdc:title ?title.
    
    OPTIONAL{
        ?creation pdc:hasTimeSpan ?timeSpan.
        ?timeSpan pdc:date ?date.
    }
            
    OPTIONAL{
    ?author pdc:wasBorn ?birth.
        OPTIONAL{
            ?birth pdc:hasTimeSpan ?birthSpan.
            ?birthSpan pdc:date ?birthDate.
        }
        OPTIONAL{
            ?birth pdc:tookPlaceAt ?birthPlace.
            ?birthPlace rdfs:label ?birthPlaceLabel.
        }
    }

    OPTIONAL{
    ?author pdc:diedIn ?death.
        OPTIONAL{
            ?death pdc:hasTimeSpan ?deathSpan.
            ?deathSpan pdc:date ?deathDate.
        }
        OPTIONAL{
            ?death pdc:tookPlaceAt ?deathPlace.
            ?deathPlace rdfs:label ?deathPlaceLabel.
        }
    }
    
    OPTIONAL{
    ?author pdc:portrait ?portrait.
    }

    OPTIONAL{
        ?agentRole pdc:authorEducationLevel ?education_level; 
    }    
        OPTIONAL{
        ?author pdc:portrait ?portrait.
    }
        OPTIONAL{
        ?author pdc:additionalName ?additionalName.
    }
        OPTIONAL{
        ?author pdc:alternativeName ?alternativeName.
    }
        OPTIONAL{
        ?author pdc:biography ?biography.
    }
        OPTIONAL{
        ?author pdc:forename ?forename.
    }
        OPTIONAL{
        ?author pdc:genName ?genName.
    }
        OPTIONAL{
        ?author pdc:ethnicity ?etn.
        ?etn rdfs:label ?ethnicity
    }
        OPTIONAL{
        ?author pdc:gender ?gen.
        ?gen rdfs:label ?gender.
    }
        OPTIONAL{
        ?author pdc:isMemberOf ?organisation.
        ?organisation rdfs:label ?organisationName.
    }
        OPTIONAL{
        ?author pdc:movement ?mov. # Literary Period!
        ?mov rdfs:label ?movement.
    }
        OPTIONAL{
        ?author pdc:religiousAffiliation ?rel.  # Religion or org?
        ?rel rdfs:label ?religion.
    }
        OPTIONAL{
        ?author pdc:nationality ?nation.
        ?nation rdfs:label ?nationality.
    }
        OPTIONAL{
        ?author pdc:hasOccupation ?occ.
        ?occ rdfs:label ?occupation.
    }
}
    ''',
    'redactions':
    '''
CONSTRUCT{

    ?poetic_work pdc:isRealisedThrough ?redaction.
    
    ?redaction pdc:title ?title;
        pdc:genre ?genre;
        pdc:text ?text;
        pdc:contributor ?contributor;
        pdc:date ?date;
        pdc:alternativeTitle ?alternativeTitle;
        pdc:scansions ?scansion.
    
    ?scansion pdc:contributor ?sc_contributor;
        pdp:typeOfScansion ?scansion_type;
        pdc:employedTechnique ?technique.
    
    ?sc_contributor pdc:name ?sc_agent_name;
        pdc:roleFunction ?sc_role.
    
    ?contributor pdc:name ?name;
        pdc:roleFunction ?role.
}

WHERE

{
    BIND (<$> AS ?poetic_work)
    ?poetic_work a pdc:PoeticWork;                                                                     
        pdc:isRealisedThrough ?redaction.
    
    OPTIONAL{
        ?redaction pdc:title ?title.
    }
    OPTIONAL{
        ?redaction pdc:genre ?genre.
    }
    OPTIONAL{
        ?redaction pdc:text ?text.
    }
    OPTIONAL{
        ?redaction pdc:alternativeTitle ?alternativeTitle.
    }

    OPTIONAL{
        ?scansion_process a pdp:ScansionProcess;
            pdp:generated ?scansion;
            pdp:usedAsInput ?redaction.
        OPTIONAL{
            ?scansion_process pdp:employedTechnique ?technique.
        }
        OPTIONAL{
            ?scansion_process pdc:hasAgentRole ?agentRole.
            ?agentRole pdc:hasAgent ?agent;
                pdc:roleFunction ?s_role.
            ?agent pdc:name ?sc_agent_name.
            ?s_role rdfs:label ?sc_role.
        }
        OPTIONAL{
            ?scansion pdp:typeOfScansion ?sc_type.
            ?sc_type rdfs:label ?scansion_type.
        }
    }

}
    ''',
    'scansion_structure':
    '''
CONSTRUCT{
    ?scansion
        pdp:stanzaList ?stanza;
        pdp:workPattern ?redaction_pattern.
    
    ?redaction_pattern
        pdp:metricalCategory ?metrical_category.

    ?stanza
        pdp:stanzaPattern ?stanza_pattern;
        pdp:content ?stanza_content;
        pdp:lineList ?line;
        pdp:typeOfStanza ?type_of_stanza;
        pdp:stanzaNumber ?stanza_number.
    
    ?line
        pdp:hasLinePattern ?line_pattern;
        pdp:relativeLineNumber ?relative_line_number;
        pdp:absoluteLineNumber ?absolute_line_number;
        pdp:content ?line_content;
        pdp:rhyme ?rhyme.
    
    ?line_pattern
        pdp:patterningMetricalScheme ?patterning_metrical_scheme.

    ?stanza_pattern
        pdp:rhymeScheme ?stanza_type.
    
    ?rhyme
        pdp:typeOfRhymeMatching ?rhyme_matching;
        pdp:rhymeLabel ?rhyme_label.
        
    # pdp:rhymeGrapheme ?rhyme_grapheme.
    
    # Q2
    ?line pdp:hasWord ?word;
        pdp:hasGrammaticalSyllable ?gram_syll;
        pdp:hasMetricalSyllable ?met_syll;
        pdp:hasPunctuation ?punctuation.
    
    ?word pdp:content ?word_content;
        pdp:isWordAnalysedBy ?word_unit;
        pdp:wordNumber ?word_number.
    
    ?gram_syll pdp:grammaticalSyllableNumber ?gram_syll_number;
        pdp:isStressed ?is_stressed_g;
        pdp:content ?gram_syll_text;
        pdp:isGrammaticalSyllableAnalysedBy ?gram_syll_unit.
    
    ?met_syll pdp:metricalSyllableNumber ?met_syll_number;
        pdp:isStressed ?is_stressed_m;
        pdp:content ?met_syll_text;
        pdp:isMetricalSyllableAnalysedBy ?met_syll_unit.
    
    # Add Metaplasm
    ?scansion pdp:enjambent ?enjambent;
        pdp:metaplasm ?metaplasm.
    
    ?enjambent pdp:affectLine ?line;
        pdp:typeOfEnjambment ?type_of_enjambment.
    
    ?metaplasm pdp:typeOfMetaplasm ?type_of_metaplasm;
        pdp:affectsFirstWord ?word.
}

WHERE{
    BIND (<$> AS ?scansion)

    ?scansion a pdp:Scansion;
        pdp:hasStanza ?stanza.
    
    ?stanza a pdp:Stanza;
        pdp:stanzaNumber ?stanza_number;
        pdp:content ?stanza_content;
        pdp:hasLine ?line.
    
    OPTIONAL{
        ?stanza pdp:typeOfStanza ?type_of_stanza.
    }
    
    ?line a pdp:Line;
        pdp:relativeLineNumber ?relative_line_number;
        pdp:absoluteLineNumber ?absolute_line_number;
        pdp:content ?line_content;
        pdp:hasWord ?word.
    
    ?word pdp:wordNumber ?word_number;
        pdp:content ?word_content.
    
    OPTIONAL{
        ?word pdp:isWordAnalysedBy ?word_unit.
    }

    OPTIONAL{
        ?word pdp:isFirstWordAffectedBy ?metaplasm.
        ?metaplasm pdp:typeOfMetaplasm ?mtp_type.
        ?mtp_type rdfs:label ?type_of_metaplasm.
    }

    OPTIONAL{
        ?line pdp:hasGrammaticalSyllable ?gram_syll.
        ?gram_syll pdp:grammaticalSyllableNumber ?gram_syll_number.
        OPTIONAL{
            ?gram_syll pdp:isStressed ?is_stressed_g.
        }
        OPTIONAL{
            ?gram_syll pdp:isGrammaticalSyllableAnalysedBy ?met_syll_unit.
        }
        OPTIONAL{
            ?line pdp:isLineAffectedBy ?enjambent.
            ?enjambent pdp:typeOfEnjambment ?enj_type.
            ?enj_type rdfs:label ?type_of_enjambment.
        }
    }

    OPTIONAL{
        ?line pdp:hasMetricalSyllable ?met_syll.
        ?met_syll pdp:isStressed ?is_stressed_m;
            pdp:metricalSyllableNumber ?met_syll_number.
    }

    OPTIONAL{
        ?line pdp:hasPunctuation ?punctuation.
        ?punctuation pdp:content ?punctuation_content.
        OPTIONAL{
            ?punctuation pdp:before ?before_word.
        }
        OPTIONAL{
            ?punctuation pdp:after ?after_word.
        }
    }

    OPTIONAL{
        ?line pdp:hasRhyme ?rhyme.
        OPTIONAL{
            ?rhyme pdp:hasRhymeMatch ?rhyme_match;
                pdp:rhymeLabel ?rhyme_label.
                # pdp:rhymeGrapheme ?rhyme_grapheme.
            ?rhyme_match pdp:typeOfRhymeMatching ?rhyme_matching_type.
            ?rhyme_matching_type rdfs:label ?rhyme_matching.
        }
    }
   
    OPTIONAL{
        ?line pdp:hasLinePattern ?line_pattern.
        ?line_pattern pdp:patterningMetricalScheme ?patterning_metrical_scheme.
    }

    OPTIONAL{
        ?stanza pdp:hasStanzaPattern ?stanza_pattern.
        ?stanza_pattern pdp:rhymeScheme ?stanza_type.
    }
}
    '''}

CONTEXT = {
    # "@language": "es",
    "author": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#author"},
    "score": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#score"},
    "name": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#name"},
    "title": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#title"},
    "deathDate": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#deathDate",
                  "@type": "http://www.w3.org/2001/XMLSchema#dateTime"},
    "roleFunction": {
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-core#roleFunction",
        "@type": "@id"},
    "birthDate": {
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-core#birthDate",
        "@type": "http://www.w3.org/2001/XMLSchema#dateTime"},
    "date": {
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-core#date",
        "@type": "http://www.w3.org/2001/XMLSchema#date"},
    "birthPlace": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#birthPlace"},
    "deathPlace": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#deathPlace"},
    "gender": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#gender" },
    "movement": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#movement" },
    "religiousAffiliation": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#religiousAffiliation" },
    "occupation": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#occupation" },
    "portrait": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#portrait" ,
                 "@type": "@id"},
    "works": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#works" },
    "ethnicity": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#ethnicity" },
    "stanzas": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasStanza",
                "@type": "@id"},
    "lines": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasLine",
              "@type": "@id"
              },
    "redactionPattern": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasRedactionPattern"},
    "stanzaPattern": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasStanzaPattern"},
    "linePattern": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasLinePattern"},
    "patterningMetricalScheme": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#patterningMetricalScheme"},
    "rhymeScheme": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#rhymeScheme"},
    "relativeLineNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#relativeLineNumber"},
    "absoluteLineNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#absoluteLineNumber"},
    "hasPunctuation": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasPunctuation",
                       "@type": "@id"},
    "isRealisedThrough": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#isRealisedThrough"},
    "text": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#text"},
    "hasMetricalSyllable": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasMetricalSyllable",
                            "@type": "@id"},
    "hasWord": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasWord",
                "@type": "@id"},
    "hasGrammaticalSyllable": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasGrammaticalSyllable",
                               "@type": "@id"},
    "grammaticalSyllableNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#grammaticalSyllableNumber"},
    "metricalSyllableNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#metricalSyllableNumber"},
    "isStressed": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isStressed"},
    "analysesWord": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#analysesWord",
                     "@type": "@id"},
    "isGrammaticalSyllableAnalysedBy": {"@id":"http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isGrammaticalSyllableAnalysedBy",
                                        "@type": "@id"},
    "isMetricalSyllableAnalysedBy": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isMetricalSyllableAnalysedBy",
                                     "@type": "@id"},
    "content": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#content"},
    "wordNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#wordNumber"},
    "scansions": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#scansions"},
    "typeOfScansion": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#typeOfScansion"},
    "employedTechnique": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#employedTechnique",
                          "@type": "@id"},
    "lineList":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#lineList"},
    "stanzaList":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#stanzaList"},
    "stanzaNumber":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#stanzaNumber"},
    "typeOfRhymeMatching":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#typeOfRhymeMatching"},
    "rhyme":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#rhyme"},
    "rhymeLabel":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#rhymeLabel"},
    "isWordAnalysedBy": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isWordAnalysedBy"},
    "enjambment": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#enjambment"},
    "affectLine": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#affectLine"},
    "typeOfEnjambment": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#typeOfEnjambment"},
    "metaplasm": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#metaplasm"},
    "typeOfMetaplasm": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#typeOfMetaplasm"},
    "affectsFirstWord": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#affectsFirstWord"}
}
