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
prefix pdc: <http://postdata.linhd.uned.es/ontology/postdata-core#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

CONSTRUCT{
    ?author pdc:portrait ?portrait;
        pdc:movement ?movement;
        pdc:name ?name;
        pdc:portrait ?portrait;
        pdc:additionalName ?additionalName;
        pdc:alternativeName ?alternativeName;
      	pdc:penName ?penName;
        pdc:biography ?biography;
        pdc:ethnicity ?ethnicity;
        pdc:gender ?gender;
        pdc:works ?poeticWork;
        pdc:birthDate ?birthDate;
        pdc:deathDate ?deathDate;
        pdc:nationality ?nationality;
        pdc:occupation ?occupation;
        pdc:birthPlace ?birthPlaceLabel;
        pdc:deathPlace ?deathPlaceLabel;
        pdc:religiousAffiliation ?religion;
    	pdc:hasDedication ?dedication_redaction;
    	pdc:isMemberOf ?organisationName;
    	pdc:socialStatus ?status;
    	pdc:literaryPeriod ?literaryPeriod;
    	pdc:assessedCertainty ?assessedCertainty;
    	pdc:authorEducationLevel ?authorEducationLevel.
  
  	?dedication_redaction pdc:title ?dedication.
    
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
    	?agentRole pdc:authorEducationLevel ?education.
    	?education rdfs:label ?authorEducationLevel.
  	}
  
  	OPTIONAL{
   		?attributeAssignment pdc:assigned ?date;
        	pdc:assignedAttributeTo ?author.
    	?certaintyAssessment pdc:assessedCertainty ?certainty;
        	pdc:isCertaintyAssessmentOf ?attributeAssignment.
    	?certainty rdfs:label ?assessedCertainty.
    	?date rdfs:type pdc:TimeSpan.
  	}
  
  	OPTIONAL{
    	?author pdc:literaryPeriod ?period.
    	?period rdfs:label ?literaryPeriod.
  	}
  
  	OPTIONAL{
    	?author pdc:socialStatus ?status.
    	?status rdfs:label ?socialStatus.
  	}
  
  	OPTIONAL{
    	?author pdc:hasDedication ?dedication_redaction.
    	?dedication_redaction pdc:title ?dedication.
  	}
    
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
        ?author pdc:penName ?penName.
    }
        OPTIONAL{
        ?author pdc:alternativeName ?alternativeName.
    }
        OPTIONAL{
        ?author pdc:biography ?biography.
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
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix pdc: <http://postdata.linhd.uned.es/ontology/postdata-core#>
prefix pdp: <http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

CONSTRUCT{

    ?poetic_work pdc:isRealisedThrough ?redaction;
        pdc:author ?ag;
    	pdc:date ?poetic_work_date;
    	pdc:literaryTradition ?literaryTradition;
    	pdc:alternativeTitle ?poetic_work_alternativeTitle;
    	pdc:poeticType ?poeticType;
    	pdc:title ?pw_title;
    	pdc:originalTitle ?pw_originalTitle;
    	pdc:subtitle ?pw_subtitle;
    	pdc:genre ?pw_genre;
    	pdc:hasNarrativeLocation ?narrativeLocation;
    	pdc:hasSynthesis ?pw_has_synthesis;
    	pdc:isSynthesisOf ?pw_is_synthesis;
    	pdc:authorship ?authorship;
    	pdc:isIntendedFor ?isIntendedFor;
    	pdc:isAbout ?entity;
    	pdc:hasDerivative ?hasDerivative;
    	pdc:isWorkOf ?isWorkOf.
  
  	?isWorkOf pdc:title ?isWorkOf_title.
  	?hasDerivative pdc:title ?hasDerivative_title.
  
  	?entity pdc:entityType ?entity_type_label;
    	pdc:entityLabel ?entity_label.
  
  	?pw_has_synthesis pdc:title ?pw_has_synthesis_title.
  	?pw_is_synthesis pdc:title ?pw_is_synthesis_title.
    
    ?ag pdc:name ?pw_agent_name;
        pdc:roleFunction ?pw_rf.
    
    ?redaction pdc:title ?title;
        pdc:genre ?redaction_genre;
        pdc:text ?text;
        pdc:date ?redaction_date;
        pdc:alternativeTitle ?redaction_alternativeTitle;
        pdc:scansions ?scansion;
    	pdc:contributor ?r_agent;
    	pdc:originalTitle ?redaction_originalTitle;
    	pdc:subtitle ?redaction_subtitle;
    	pdc:hasLanguage ?hasLanguage;
    	pdc:typeOfTextualElement ?typeOfTextualElement;
    	pdc:mentions ?mentioned_entity;
    	pdc:typeOfRedaction ?typeOfRedaction;
    	pdc:dedicatedTo ?dedicatedTo;
    	pdc:audienceEducationLevel ?audienceEducationLevel;
    	pdc:isRepresentativeExpressionFor ?representative_pw;
    	pdc:hasTranslation ?has_translation_redaction;
    	pdc:isTranslationOf ?is_translation_redaction;
    	pdc:incorporates ?incorporates_redaction;
    	pdc:isIncorporatedIn ?is_incorporated_redaction;
    	pdc:audience ?audience;
    	pdc:hasCommentary ?hasCommentary;
    	pdc:hasIncipit ?hasIncipit;
    	pdc:hasExicipt ?hasExcipit.
  
    ?is_incorporated_redaction pdc:title ?is_incorporated_redaction_title.
    ?incorporates_redaction pdc:title ?incorporates_redaction_title.
    ?is_translation_redaction pdc:title ?is_translation_redaction_title.
    ?has_translation_redaction pdc:title ?has_translation_redaction_title.
    ?representative_pw pdc:title ?representative_pw_title.
  
  	?mentioned_entity pdc:entityType ?mentioned_entity_type_label;
    	pdc:entityLabel ?mentioned_entity_label.
  
  	?r_agent pdc:name ?redaction_agent_name;
    	pdc:roleFunction ?redaction_agent_role.
    
    ?scansion pdc:contributor ?sc_contributor;
        pdp:typeOfScansion ?scansion_type;
        pdc:employedTechnique ?technique;
        pdp:id ?scansion_id.
    
    ?sc_contributor pdc:name ?sc_agent_name;
        pdc:roleFunction ?sc_role.
}

WHERE

{
    BIND (<$> AS ?poetic_work)
    ?poetic_work a pdc:PoeticWork;                                                                     
        pdc:isRealisedThrough ?redaction.
         
    OPTIONAL{
        ?poetic_work pdc:wasInitiatedBy ?event.
        ?event pdc:hasAgentRole ?ag.
        ?ag pdc:hasAgent ?pw_agent.
        ?pw_agent pdc:name ?pw_agent_name.
        ?ag pdc:roleFunction ?pw_rf.
        ?pw_rf rdfs:label ?pw_role.
    }
  
  OPTIONAL{
   	?redaction pdc:hasCommentary ?hasCommentary. 
  }
  
  OPTIONAL{
  	?redaction pdc:hasExcipit ?hasExcipit. 
  }
  
  OPTIONAL{
   	?redaction pdc:hasIncipit ?hasIncipit. 
  }
  
  OPTIONAL{
    ?redaction pdc:audience ?audience_concept.
    ?audience_concept rdfs:label ?audience.
  }
  
   OPTIONAL{
   	?redaction pdc:isIncorporatedIn ?is_incorporated_redaction.
    ?is_incorporated_redaction pdc:title ?is_incorporated_redaction_title.
  }
  
  OPTIONAL{
   	?redaction pdc:incorporates ?incorporates_redaction.
    ?incorporates_redaction pdc:title ?incorporates_redaction_title.
  }
  
  OPTIONAL{
   	?redaction pdc:isTranslationOf ?is_translation_redaction.
    ?is_translation_redaction pdc:title ?is_translation_redaction_title.
  }
  
  OPTIONAL{
   	?redaction pdc:hasTranslation ?has_translation_redaction.
    ?has_translation_redaction pdc:title ?has_translation_redaction_title.
  }
  
  OPTIONAL{
   	?redaction pdc:isRepresentativeExpressionFor ?representative_pw.
    ?representative_pw pdc:title ?representative_pw_title.
  }
  
  OPTIONAL{
   	?redaction pdc:audienceEducationLevel ?audienceLevel.
    ?audienceLevel rdfs:label ?audienceEducationLevel.
  }
  OPTIONAL{
   	?redaction pdc:dedicatedTo ?dedicated_redaction.
    ?dedicated_redaction pdc:name ?dedicatedTo.
  }
  OPTIONAL{
   	?redaction pdc:typeOfRedaction ?redaction_type.
    ?redaction_type rdfs:label ?typeOfRedaction.
  }
  
  OPTIONAL{
   	?redaction pdc:mentions ?mentioned_entity.
  	?mentioned_entity pdc:entityType ?mentioned_entity_type_label;
    	pdc:entityLabel ?mentioned_entity_label. 
  }
  OPTIONAL{
  	?redaction pdc:hasLanguage ?redaction_language.
    ?redaction_language rdfs:label ?hasLanguage.
  }  
  OPTIONAL{
  	?redaction pdc:typeOfTextualElement ?textualElement.
    ?textualElement rdfs:label ?typeOfTextualElement.
  }
  OPTIONAL{
   	?redaction pdc:subtitle ?redaction_subtitle. 
  }
    OPTIONAL{
   	?redaction pdc:originalTitle ?redaction_originalTitle. 
  }
  
  OPTIONAL{
   	?poetic_work pdc:isWorkOf ?isWorkOf.
    ?isWorkOf pdc:title ?isWorkOf_title.
  }
  
  OPTIONAL{
   	?poetic_work pdc:hasDerivative ?hasDerivative.
    ?hasDerivative pdc:title ?hasDerivative_title.
  }
  
  OPTIONAL{
   	?poetic_work pdc:isAbout ?entity.
    ?entity rdf:type ?entity_type.
  	?entity_type rdfs:label ?entity_type_label.
    ?entity rdfs:label ?entity_label.
  }
  
  OPTIONAL{
   	?poetic_work pdc:isIntendedFor ?intended_person.
    ?intended_person pdc:name ?isIntendedFor.
  }
  
  OPTIONAL{
   	?poetic_work pdc:authorship ?_authorship.
    ?_authorship rdfs:label ?authorship.
  }
  
  	OPTIONAL{
    	?poetic_work pdc:hasSynthesis ?pw_has_synthesis.
    	?pw_has_synthesis pdc:title ?pw_has_synthesis_title.
  	}
  
  OPTIONAL{
    	?poetic_work pdc:isSynthesisOf ?pw_is_synthesis.
    	?pw_is_synthesis pdc:title ?pw_is_synthesis_title.
  	}
  
  	OPTIONAL{
    	?poetic_work pdc:hasNarrativeLocation ?narrativeLocation.
  	}
  
  	OPTIONAL{
    	?poetic_work pdc:originalTitle ?pw_originalTitle.
  	}
  	OPTIONAL{
    	?poetic_work pdc:title ?pw_title.
  	}
  
  	OPTIONAL{
    	?poetic_work pdc:subtitle ?pw_subtitle.
  	}
  
  	OPTIONAL{
    	?poetic_work pdc:genre ?pw_genre.
  	}
  
  	OPTIONAL{
    	?poetic_work pdc:poeticType ?poetic_type.
    	?poetic_type rdfs:label ?poeticType.
  	}
  
  	OPTIONAL{
    	?poetic_work pdc:literaryTradition ?tradition.
    	?tradition rdfs:label ?literaryTradition.
  	}
  
  	OPTIONAL{
    	?poetic_work pdc:alternativeTitle ?poetic_work_alternativeTitle.
  	}
  
  	OPTIONAL{
    	?redaction pdc:wasCreatedByExpressionCreationForExpression ?ex_creation.
    	?ex_creation pdc:hasAgent ?r_agent.
    	?r_agent pdc:name ?redaction_agent_name.
    	?r_agent pdc:roleFunction ?redaction_agent_role.
  	}
    
    OPTIONAL{
        ?redaction pdc:title ?title.
    }
    OPTIONAL{
        ?redaction pdc:genre ?redaction_genre.
    }
    OPTIONAL{
      ?redaction pdc:text ?text.
    }
    OPTIONAL{
      ?redaction pdc:alternativeTitle ?redaction_alternativeTitle.
    }
  	OPTIONAL{
    	?creation pdc:initiated ?poetic_work;
               pdc:hasTimeSpan ?sp.
    	?sp pdc:date ?poetic_work_date.
  	}
  	OPTIONAL{
    	?creation pdc:createdExpressionFromExpressionCreation ?redaction;
               pdc:hasTimeSpan ?sp.
    	?sp pdc:date ?redaction_date.
  	}

  	OPTIONAL{
      ?scansion_process a pdp:ScansionProcess;
          pdp:generated ?scansion;
          pdp:usedAsInput ?redaction.
  	}
        
    OPTIONAL{
        ?scansion_process pdp:employedTechnique ?technique.
    }
        
    OPTIONAL{
        ?scansion_process pdc:hasAgentRole ?sc_contributor.
        ?sc_contributor pdc:hasAgent ?agent;
            pdc:roleFunction ?s_role.
    }
    
    OPTIONAL{
        ?agent pdc:name ?sc_agent_name.
    }
    OPTIONAL{
        ?s_role rdfs:label ?sc_role.
    }
    OPTIONAL{
        ?agent rdfs:label ?sc_agent_name.
    }

        
    OPTIONAL{
        ?scansion pdp:typeOfScansion ?sc_type.
        ?sc_type rdfs:label ?scansion_type.
    }
        
    OPTIONAL{
        ?scansion pdp:id ?scansion_id.
    }

}
    ''',
    'scansion_structure':
    '''    

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
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-core#roleFunction"},
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
    "redactions": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#isRealisedThrough"},
    "text": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#text"},
    "metricalSyllableList": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasMetricalSyllable",
                            "@type": "@id"},
    "wordList": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasWord",
                "@type": "@id"},
    "grammaticalSyllableList": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasGrammaticalSyllable",
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
    "employedTechnique": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#employedTechnique"},
    "lineList":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#lineList"},
    "stanzaList":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#stanzaList"},
    "stanzaNumber":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#stanzaNumber"},
    "typeOfRhymeMatching":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#typeOfRhymeMatching"},
    "rhyme":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#rhyme"},
    "rhymeLabel":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#rhymeLabel"},
    "isWordAnalysedBy": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isWordAnalysedBy",
                         "@type": "@id"},
    "enjambment": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#enjambment"},
    "affectLine": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#affectLine",
                   "@type": "@id"},
    "typeOfEnjambment": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#typeOfEnjambment"},
    "metaplasm": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#metaplasm"},
    "typeOfMetaplasm": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#typeOfMetaplasm"},
    "affectsFirstWord": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#affectsFirstWord",
                         "@type": "@id"},
    "affectsLine": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#affectsLine",
                    "@type": "@id"},
    "file_id": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#id"},
    "contributor": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#contributor",
                    "@type": "@id"}
}
