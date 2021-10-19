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
    'author_profile':
    '''# This query returns a set of information for an author
# Inlucdes personal information
# Organisations the person may belong to
# Poetic works and the number of editions for each work

CONSTRUCT{
    <$> pdc:portrait ?portrait;
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
        pdc:religiousAffiliation ?religion.
    
    ?poeticWork  pdc:roleFunction ?role;
        pdc:title ?title;
        pdc:date ?date;
}

WHERE{
    <$> pdc:isAgentOf ?agentRole;
        pdc:name ?name.
    
    ?creation pdc:hasAgentRole ?agentRole;
        pdc:initiated ?poeticWork;
        a pdc:WorkConception.
    
    ?agentRole pdc:roleFunction ?role;
        pdc:hasAgent <$>.
    
    ?poeticWork pdc:title ?title.
    
    OPTIONAL{
        ?creation pdc:hasTimeSpan ?timeSpan.
        ?timeSpan pdc:date ?date.
    }
            
    OPTIONAL{
	<$> pdc:wasBorn ?birth.
    	?birth pdc:hasTimeSpan ?birthDate;
        pdc:tookPlaceAt ?birthPlace.
    }

    OPTIONAL{
	<$> pdc:diedIn ?death.    
    	?death pdc:hasTimeSpan ?deathDate;
        pdc:tookPlaceAt ?deathPlace.
    }
    
    OPTIONAL{
	<$> pdc:portrait ?portrait.
    }

    OPTIONAL{
        ?agentRole pdc:authorEducationLevel ?education_level; 
    }    
        OPTIONAL{
        <$> pdc:portrait ?portrait.
    }
        OPTIONAL{
        <$> pdc:additionalName ?additionalName.
    }
        OPTIONAL{
        <$> pdc:alternativeName ?alternativeName.
    }
        OPTIONAL{
        <$> pdc:biography ?biography.
    }
        OPTIONAL{
        <$> pdc:forename ?forename.
    }
        OPTIONAL{
        <$> pdc:genName ?genName.
    }
        OPTIONAL{
        <$> pdc:ethnicity ?etn.
        ?etn rdfs:label ?ethnicity
    }
        OPTIONAL{
        <$> pdc:gender ?gen.
        ?gen rdfs:label ?gender.
    }
        OPTIONAL{
        <$> pdc:isMemberOf ?organisation.
        ?organisation rdfs:label ?organisationName.
    }
        OPTIONAL{
        <$> pdc:movement ?mov. # Literary Period!
        ?mov rdfs:label ?movement.
    }
        OPTIONAL{
        <$> pdc:religiousAffiliation ?rel.  # Religion or org?
        ?rel rdfs:label ?religion.
    }
        OPTIONAL{
        <$> pdc:nationality ?nation.
        ?nation rdfs:label ?nationality.
    }
        OPTIONAL{
        <$> pdc:occupation ?occ.
        ?occ rdfs:label ?occupation.
    }
}
    ''',
    'redactions':
    '''
CONSTRUCT{

    <$> pdc:isRealisedThrough ?redaction.
    
    ?redaction pdc:title ?title;
        pdc:genre ?genre;
        pdc:text ?text;
        pdc:contributor ?contributor;
        pdc:date ?date;
        pdc:alternativeTitle ?alternativeTitle.
    
    ?contributor pdc:name ?name;
        pdc:roleFunction ?role.
}
WHERE
{
    <$> a pdc:PoeticWork;
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
        ?creation a pdc:ExpressionCreation;
            pdc:createdExpressionFromExpressionCreation ?redaction;
            pdc:hasAgentRole ?agentRole;
            pdc:hasTimeSpan ?timeSpan.
        ?timeSpan pdc:date ?date.
        ?agentRole pdc:hasAgent ?agent;
            pdc:roleFunction ?role.
        ?agent pdc:name ?name.
    }
}
    ''',
    'scansion_structure':
    '''
CONSTRUCT{
    ?redaction
        pdp:hasStanza ?stanza;
        pdp:hasRedactionPattern ?redaction_pattern.
    
    ?redaction_pattern
        pdp:metricalCategory ?metrical_category.

    ?stanza
        pdp:hasStanzaPattern ?stanza_pattern;
        pdp:hasLine ?line.
    
    ?line
        pdp:hasLinePattern ?line_pattern;
        pdp:relativeLineNumber ?relative_line_number;
        pdp:absoluteLineNumber ?absolute_line_number.
    
    ?line_pattern
        pdp:patterningMetricalScheme ?patterning_metrical_scheme.

    ?stanza_pattern
        pdp:rhymeScheme ?stanza_type.
    
    ?rhyme
        pdp:typeOfRhymeMatching ?rhyme_matching_type;
        pdp:rhymeLabel ?rhyme_label;
        pdp:rhymeGrapheme ?rhyme_grapheme.
}

WHERE{

    # ?scansion_process a pdp:ScansionProcess;
        # pdp:generated ?scansion;
        # pdp:usedAsInput ?redaction;
        # pdp:hasAgent ?agent.
    
    #  OPTIONAL{
    #     ?scansion_process pdp:usedAsInput ?redaction.
    # }
    
    # ?scansion a pdp:Scansion;
        # pdp:typeOfScansion ?type_of_scansion.

    BIND (<$> AS ?redaction)
    
    OPTIONAL{
        ?redaction pdp:hasRedactionPattern ?redaction_pattern.
        ?redaction_pattern a pdp:RedactionPattern;
            pdp:metricalCategory ?metrical_category;
            pdp:metricalComplexity ?metrical_complexity.
        # ?scansion pdp:hasPatternAnnotation ?redaction_pattern.
    }

    ?redaction a pdc:Redaction;
        pdp:hasStanza ?stanza.
    
    ?stanza a pdp:Stanza;
        pdp:hasStanzaPattern ?stanza_pattern;
        pdp:stanzaNumber ?stanza_number;
        pdp:content ?stanza_content;
        pdp:hasLine ?line.
    
    ?line a pdp:Line;
        pdp:hasLinePattern ?line_pattern;
        pdp:relativeLineNumber ?relative_line_number;
        pdp:absoluteLineNumber ?absolute_line_number;
        pdp:content ?line_content.
    
    OPTIONAL{
        # ?scansion pdp:hasPatternAnnotation ?stanza_pattern.
        ?stanza_pattern a pdp:StanzaPattern;
            pdp:rhymeScheme ?stanza_type.
    }
    OPTIONAL{
        # ?scansion pdp:hasPatternAnnotation ?line_pattern.
        ?line_pattern a pdp:LinePattern;
            pdp:patterningMetricalScheme ?patterning_metrical_scheme.
    }
    OPTIONAL{
        ?line pdp:hasRhyme ?rhyme.
        ?rhyme pdp:typeOfRhymeMatching ?type_of_rm;
            pdp:rhymeLabel ?rhyme_label;
            pdp:rhymeGrapheme ?rhyme_grapheme.
        ?type_of_rm rdfs:label ?rhyme_matching_type.
    }
}
    ''',
    'scansion_line':
    '''
CONSTRUCT{
    <$> pdp:hasWord ?word;
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
}

WHERE{
    <$> a pdp:Line.
    
    OPTIONAL{
        <$> pdp:hasMetricalSyllable ?met_syll.
        ?met_syll pdp:isStressed ?is_stressed_m;
            pdp:metricalSyllableNumber ?met_syll_number;
            pdp:content ?met_syll_text.
        OPTIONAL{
            ?met_syll pdp:isMetricalSyllableAnalysedBy ?met_syll_unit.
        }
    }
    OPTIONAL{
        <$> pdp:hasGrammaticalSyllable ?gram_syll.
        ?gram_syll pdp:grammaticalSyllableNumber ?gram_syll_number;
            # pdp:analysesWord ?word;
            pdp:isStressed ?is_stressed_g;
            pdp:content ?gram_syll_text.
        OPTIONAL{
            ?gram_syll pdp:isGrammaticalSyllableAnalysedBy ?gram_syll_unit.
        }
    }
    OPTIONAL{
        <$> pdp:hasWord ?word.
        ?word pdp:wordNumber ?word_number;
            pdp:isWordAnalysedBy ?word_unit;
            pdp:content ?word_content.
        OPTIONAL{
            ?word pdp:isWordAnalysedBy ?word_unit.
        }
    }
    OPTIONAL{
        <$> pdp:hasPunctuation ?punctuation.
        ?punctuation pdp:after ?after_word.
    }
    OPTIONAL{
        <$> pdp:hasPunctuation ?punctuation.
        ?punctuation pdp:before ?before_word.
    }
}
    '''
}

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
    "gender": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#gender" },
    "movement": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#movement" },
    "religiousAffiliation": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#religiousAffiliation" },
    "occupation": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#occupation" },
    "portrait": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#portrait" },
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
    "wordNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#wordNumber"}
}
