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
        PREFIX kos: <http://postdata.linhd.uned.es/kos/>

        # Construct includes properties that are not in the ontology, but used to put names to the keys
        CONSTRUCT {
            ?work   pdc:score ?sc;
                    pdc:name ?resultText;
                    pdc:author ?creator;
                    pdc:date ?date.
        }
                
        WHERE{
            SELECT ?work ?sc ?resultText ?creator ?date WHERE {

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

                ?resultText bif:contains '"$*"' option (score ?sc).

            }
        }
        order by desc(?sc)
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
        prefix pdc: <http://postdata.linhd.uned.es/ontology/postdata-core#>

        CONSTRUCT {
            ?person pdc:score ?sc;
                pdc:name ?resultText;
                pdc:birthDate ?birthDate;
                pdc:deathDate ?deathDate;
                pdc:deathPlace ?deathPlaceLabel;
                pdc:birthPlace  ?birthPlaceLabel.
                
        }
        
        
        WHERE {
            ?person pdc:name ?resultText.
            ?person a pdc:Person.
            ?resultText bif:contains '"$*"' option (score ?sc).
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
        order by desc(?sc)
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
    
    ?poeticWork  pdc:roleFunction ?roleLabel;
        pdc:title ?title;
        pdc:date ?date.
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
        
    ?role rdfs:label ?roleLabel.
    
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
        ?agentRole pdc:authorEducationLevel ?education_level.
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
        ?etn rdfs:label ?ethnicity.
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
    
    ?ag pdc:hasAgent ?pw_agent;
        pdc:roleFunction ?pw_role.
    
    ?pw_agent pdc:name ?pw_agent_name.
    
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
        pdp:id ?scansion_id;
        pdp:graphName ?scansion_graph.
    
    ?sc_contributor pdc:name ?sc_agent_name;
        pdc:roleFunction ?sc_role.
}
WHERE
{
    BIND (<$> AS ?poetic_work)
    ?poetic_work a pdc:PoeticWork;                                                                     
        pdc:isRealisedThrough ?redaction.
  
  	?scansion_process a pdp:ScansionProcess;
        pdp:generated ?scansion;
        pdp:usedAsInput ?redaction.
  
    OPTIONAL{
      ?scansion pdp:typeOfScansion ?sc_type.
      ?sc_type rdfs:label ?scansion_type.
    }
    OPTIONAL{
      ?scansion pdp:id ?scansion_id.
    }
    OPTIONAL{
      ?scansion pdp:graphName ?scansion_graph.
    }
    OPTIONAL{
      ?scansion_process pdp:employedTechnique ?technique.
    }
    OPTIONAL{
      ?scansion_process pdc:hasAgentRole ?sc_contributor.
      ?sc_contributor pdc:hasAgent ?agent;
                      pdc:roleFunction ?s_role.
      ?s_role rdfs:label ?sc_role.
      OPTIONAL{
        ?agent rdfs:label ?sc_agent_name.
      }
      OPTIONAL{
        ?agent pdc:name ?sc_agent_name.
      }
    }
         
    OPTIONAL{
        ?poetic_work pdc:wasInitiatedBy ?event.
        ?event pdc:hasAgentRole ?ag.
        ?ag pdc:hasAgent ?pw_agent.
        ?pw_agent pdc:name ?pw_agent_name.
        ?ag pdc:roleFunction ?pw_rf.
        ?pw_rf rdfs:label ?pw_role.
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
 }
    ''',
    "scansion_graph":
    '''
    CONSTRUCT {?s ?p ?o}
    FROM <$>
    WHERE{?s ?p ?o}
    ''',
    "scansion_query":
    '''

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX pdc: <http://postdata.linhd.uned.es/ontology/postdata-core#>
PREFIX pdp: <http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

CONSTRUCT{
    ?scansion
        pdp:stanzaList ?stanza;
    	pdp:hasRefrain ?hasRefrain;
    	pdp:interStrophicRelations ?interStrophicRelations;
    	pdp:isIsometric ?isIsometric;
    	pdp:isIsotrophic ?isIsotrophic;
    	pdp:isUnissonant ?isUnissonant;
    	pdp:rhymeTypeProportion ?rhymeTypeProportion;
    	pdp:metricalCategory ?metricalCategory;
    	pdp:metricalComplexity ?metricalComplexity;
    	pdp:metricalContext ?metricalContext;
    	pdp:versificationType ?versificationType;
    	pdp:acrostic ?acrostic;
    	pdp:scheme ?scheme;
    	pdp:trope ?trope.

    ?stanza
        pdp:content ?stanza_content;
        pdp:lineList ?line;
        pdp:typeOfStanza ?type_of_stanza;
        pdp:stanzaNumber ?stanza_number;
        pdp:rhymeScheme ?stanza_type;
        pdp:metricalType ?metrical_type;
    	pdp:altRhymeScheme ?altRhymeScheme;
    	pdp:clausulaScheme ?clausulaScheme;
    	pdp:clausulaSchemeType ?clausulaSchemeType;
 		pdp:rhymeDispositionType ?rhymeDispositionType;
    	pdp:paraphrasis ?paraphrasis;
    	pdp:metricalNotes ?stanza_metricalNotes;
    	pdp:isMetricStanza ?isMetricStanza;
    	pdp:typeOfStanzaEdition ?typeOfStanzaEdition.

    ?line
        pdp:patterningMetricalScheme ?patterning_metrical_scheme;
        pdp:relativeLineNumber ?relative_line_number;
        pdp:absoluteLineNumber ?absolute_line_number;
        pdp:content ?line_content;
        pdp:accentedVowelsPattern ?accentedVowelsPattern;
      	pdp:accentedVowels ?accentedVowels ;
      	pdp:altPatterningMetricalScheme  ?altPatterningMetricalScheme ;
        pdp:lineMinLength ?lineMinLength ;
        pdp:lineMaxLength ?lineMaxLength ;
        pdp:isHypermetre ?isHypermetre ;
        pdp:isHypometre ?isHypometre ;
        pdp:isRegular ?isRegular ;
        pdp:firstHemistich ?firstHemistich ;
        pdp:secondHemistich ?secondHemistich ;
        pdp:isRefrain ?isRefrain ;
        pdp:hasAnacrusis ?hasAnacrusis ;
        pdp:hasCaesura ?hasCaesura ;
        pdp:initialPhonemesPattern ?initialPhonemesPattern ;
        pdp:initialPhonemesPatternByManner ?initialPhonemesPatternByManner ;
        pdp:phonemePattern ?phonemePattern ;
        pdp:phonemePatternByManner ?phonemePatternByManner ;
        pdp:grammaticalStressPattern ?grammaticalStressPattern ;
        pdp:scannedLine ?scannedLine ;
        pdp:feetType ?feetType ;
        pdp:vowelTypeScheme ?vowelTypeScheme ;
        pdp:syllabicMetricalLength ?syllabicMetricalLength;
        pdp:altSyllabicMetricalLength ?altSyllabicMetricalLength;
        pdp:moraeMetricalScheme ?moraeMetricalScheme ;
        pdp:altMoraeMetricalScheme ?altMoraeMetricalScheme;
        pdp:lineMaxlength ?lineMaxLength;
        pdp:lineMinLength ?lineMinLength.

    # Q2
    ?line pdp:hasWord ?word;
        # pdp:hasGrammaticalSyllable ?gram_syll;
        pdp:hasMetricalSyllable ?met_syll;
        pdp:hasPunctuation ?punctuation;
        pdp:rhymeLabel ?rhyme_label.

    ?line pdp:isEchoLineIn ?rhymeMatch_echo;
        pdp:isCallLineIn ?rhymeMatch_call.

    ?rhymeMatch_call pdp:rhymeGrapheme ?rhyme_grapheme_call;
        pdp:typeOfRhymeMatching ?rhyme_matching_type_call;
        pdp:echoLineNumber ?echo_line_number.

    ?rhymeMatch_echo pdp:rhymeGrapheme ?rhyme_grapheme_echo;
        pdp:typeOfRhymeMatching ?rhyme_matching_type_echo;
        pdp:callLineNumber ?call_line_number.

    ?punctuation pdp:content ?punctuation_content;
        pdp:beforeWordNumber ?before_word_number;
        pdp:afterWordNumber ?after_word_number.

    ?word pdp:content ?word_content;
        pdp:isWordAnalysedBy ?word_unit;
        pdp:wordNumber ?word_number;
    	pdp:ending ?ending;
      	pdp:lemma ?lemma;
  		pdp:morphologicalAnnotation ?morphologicalAnnotation ;
  		pdp:partOfSpeech ?partOfSpeech ;
  		pdp:translation ?translation.

    ?gram_syll pdp:grammaticalSyllableNumber ?gram_syll_number;
        pdp:isStressed ?is_stressed_g;
        pdp:content ?gram_syll_text;
        # pdp:isGrammaticalSyllableAnalysedBy ?gram_syll_unit.
        pdp:isGrammaticalSyllableAnalysedBy ?gram_syll_unit_number.

    ?met_syll pdp:metricalSyllableNumber ?met_syll_number;
        pdp:isStressed ?is_stressed_m;
        pdp:content ?met_syll_text;
        pdp:isMetricalSyllableAnalysedBy ?met_syll_unit. # We don't have this in spanish meter.

    ?line pdp:isLineAffectedBy ?enjambment.
    ?enjambment pdp:typeOfEnjambment ?type_of_enjambment.

    ?gram_syll pdp:isFirsGrammaticalSyllableAffectedBy ?metaplasm.
    ?metaplasm pdp:typeOfMetaplasm ?type_of_metaplasm;
        pdp:metaplasmIndex ?metaplasm_index.

  	?acrostic pdp:typeOfAcrostic ?typeOfAcrostic;
    	pdp:hasStartingLine ?acrosticStartingLine;
    	pdp:hasEndingLine ?acrosticEndingLine.

    ?scheme pdp:typeOfScheme ?typeOfScheme;
    	pdp:hasStartingLine ?schemeStartingLine;
    	pdp:hasEndingLine ?schemeEndingLine.

    ?trope pdp:typeOfTrope ?typeOfTrope;
    	pdp:hasStartingLine ?tropeStartingLine;
    	pdp:hasEndingLine ?tropeEndingLine.
}

FROM <$>
WHERE{
    ?scansion
        pdp:hasStanza ?stanza.

    ?stanza a pdp:Stanza;
        pdp:stanzaNumber ?stanza_number;
        pdp:content ?stanza_content;
        pdp:hasLine ?line.

  	OPTIONAL{
    	?scansion pdp:hasDeviceAnnotation ?acrostic.
    	?acrostic rdf:type pdp:Acrostic;
        	pdp:isAcrosticPresentAt ?acrostic_excerpt;
         	pdp:typeOfAcrostic ?typeOfAcrosticConcept.
    	?typeOfAcrosticConcept rdfs:label ?typeOfAcrostic.
    	?acrostic_excerpt pdp:hasStartingLine ?acrosticStartingLine;
                       	pdp:hasEndingLine ?acrosticEndingLine.
  	}
    	OPTIONAL{
    	?scansion pdp:hasDeviceAnnotation ?scheme.
    	?scheme rdf:type pdp:Scheme;
        	pdp:isSchemePresentAt ?scheme_excerpt;
         	pdp:typeOfScheme ?typeOfSchemeConcept.
    	?typeOfSchemeConcept rdfs:label ?typeOfScheme.
    	?scheme_excerpt pdp:hasStartingLine ?schemeStartingLine;
                       	pdp:hasEndingLine ?schemeEndingLine.
  	}
      	OPTIONAL{
    	?scansion pdp:hasDeviceAnnotation ?trope.
    	?trope rdf:type pdp:Trope;
        	pdp:isTropePresentAt ?trope_excerpt;
         	pdp:typeOfTrope ?typeOfTropeConcept.
    	?typeOfTropeConcept rdfs:label ?typeOfTrope.
    	?trope_excerpt pdp:hasStartingLine ?tropeStartingLine;
                       	pdp:hasEndingLine ?tropeEndingLine.
  	}
    OPTIONAL{
    	?line pdp:lineMaxlength ?lineMaxLength;
    	    pdp:lineMinLength ?lineMinLength.
  	}
  	OPTIONAL{
    	?line pdp:syllabicMetricalLength ?syllabicMetricalLength.
  	}
    OPTIONAL{
    	?line pdp:altSyllabicMetricalLength ?altSyllabicMetricalLength.
  	}
  	OPTIONAL{
    	?word pdp:ending ?ending.
  	}
  	OPTIONAL{
    	?word pdp:lemma ?lemma.
  	}
  	  	OPTIONAL{
    	?word pdp:morphologicalAnnotation ?morphologicalAnnotation.
  	}
        	OPTIONAL{
    	?word pdp:partOfSpeech ?partOfSpeech.
  	}
        	OPTIONAL{
    	?word pdp:translation ?translation.
  	}
  	OPTIONAL{
    	?line pdp:accentedVowelsPattern ?accentedVowelsPattern.
  	}
        	OPTIONAL{
    	?line pdp:accentedVowels ?accentedVowels.
  	}
        	OPTIONAL{
    	?line pdp:altPatterningMetricalScheme ?altPatterningMetricalScheme.
  	}
        	OPTIONAL{
    	?line pdp:lineMinLength ?lineMinLength.
  	}
        	OPTIONAL{
    	?line pdp:lineMaxLength ?lineMaxLength.
  	}
        	OPTIONAL{
    	?line pdp:isHypermetre ?isHypermetre.
  	}
        	OPTIONAL{
    	?line pdp:isHypometre ?isHypometre.
  	}
        	OPTIONAL{
    	?line pdp:isRegular ?isRegular.
  	}
        	OPTIONAL{
    	?line pdp:firstHemistich ?firstHemistich.
  	}
        	OPTIONAL{
    	?line pdp:secondHemistich ?secondHemistich.
  	}
        	OPTIONAL{
    	?line pdp:isRefrain ?isRefrain.
  	}
        	OPTIONAL{
    	?line pdp:hasAnacrusis ?hasAnacrusis.
  	}
        	OPTIONAL{
    	?line pdp:hasCaesura ?hasCaesura.
  	}
        	OPTIONAL{
    	?line pdp:initialPhonemesPattern ?initialPhonemesPattern.
  	}
        	OPTIONAL{
    	?line pdp:initialPhonemesPatternByManner ?initialPhonemesPatternByManner.
  	}
        	OPTIONAL{
    	?line pdp:phonemePattern ?phonemePattern.
  	}
        	OPTIONAL{
    	?line pdp:phonemePatternByManner ?phonemePatternByManner.
  	}
        	OPTIONAL{
    	?line pdp:grammaticalStressPattern ?grammaticalStressPattern.
  	}
        	OPTIONAL{
    	?line pdp:scannedLine ?scannedLine.
  	}
        	OPTIONAL{
    	?line pdp:feetType ?feetType.
  	}
        	OPTIONAL{
    	?line pdp:vowelTypeScheme ?vowelTypeScheme.
  	}
        	OPTIONAL{
    	?line pdp:moraeMetricalScheme ?moraeMetricalScheme.
  	}
        	OPTIONAL{
    	?line pdp:altMoraeMetricalScheme ?altMoraeMetricalScheme.
  	}
     OPTIONAL{
    	?stanza pdp:altRhymeScheme ?altRhymeScheme.
  	}
        	OPTIONAL{
    	?stanza pdp:clausulaScheme ?clausulaScheme.
  	}
        	OPTIONAL{
    	?stanza pdp:clausulaSchemeType ?clausulaSchemeTypeConcept.
    	?clausulaSchemeTypeConcept rdfs:label ?clausulaSchemeType.
  	}
        	OPTIONAL{
    	?stanza pdp:rhymeDispositionType ?rhymeDispositionTypeConcept.
    	?rhymeDispositionTypeConcept rdfs:label ?rhymeDisposition.
  	}
        	OPTIONAL{
    	?stanza pdp:paraphrasis ?paraphrasis.
  	}
        	OPTIONAL{
    	?stanza pdp:metricalNotes ?stanza_metricalNotes.
  	}
        	OPTIONAL{
    	?stanza pdp:isMetricStanza ?isMetricStanza.
  	}
        	OPTIONAL{
    	?stanza pdp:typeOfStanzaEdition ?typeOfStanzaEditionConcept.
    	?typeOfStanzaEditionConcept rdfs:label ?typeOfStanzaEdition.
  	}


  	OPTIONAL{
    	?scansion pdc:hasRefrain ?hasRefrain.
  	}
    	OPTIONAL{
    	?scansion pdc:interStrophicRelations ?interStrophicRelations.
  	}
    	OPTIONAL{
    	?scansion pdc:isIsometric ?isIsometric.
  	}
    	OPTIONAL{
    	?scansion pdc:isIsotrophic ?isIsotrophic.
  	}
    	OPTIONAL{
    	?scansion pdc:isUnissonant ?isUnissonant.
  	}
    	OPTIONAL{
    	?scansion pdc:rhymeTypeProportion ?rhymeTypeProportion.
  	}
    	OPTIONAL{
    	?scansion pdc:metricalCategory ?metricalCategoryConcept.
    	?metricalCategoryConcept rdfs:label ?metricalCategory.
  	}
    	OPTIONAL{
    	?scansion pdc:metricalComplexity ?metricalComplexityConcept.
    	?metricalComplexityConcept rdfs:label ?metricalComplexity.
  	}
    	OPTIONAL{
    	?scansion pdc:metricalContext ?metricalContextConcept.
    	?metricalContextConcept rdfs:label ?metricalContext.
  	}
    	OPTIONAL{
    	?scansion pdc:versificationType ?versificationTypeConcept.
    	?versificationTypeConcept rdfs:label ?versificationType.
  	}

    OPTIONAL{
        ?stanza pdp:typeOfStanza ?type_of_stanza.
    }
    OPTIONAL{
        ?stanza pdp:metricalType ?mt.
        ?mt rdfs:label ?metrical_type.
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
        ?line pdp:hasGrammaticalSyllable ?gram_syll.
        ?gram_syll pdp:grammaticalSyllableNumber ?gram_syll_number.
    }
    OPTIONAL{
            ?gram_syll pdp:isStressed ?is_stressed_g.
    }
    OPTIONAL{
            ?gram_syll pdp:content ?gram_syll_text.
    }
    OPTIONAL{
            ?gram_syll pdp:isGrammaticalSyllableAnalysedBy ?gram_syll_unit.
            ?gram_syll_unit pdp:metricalSyllableNumber ?gram_syll_unit_number.
    }

    OPTIONAL{
            ?line pdp:isLineAffectedBy ?enjambment.
            ?enjambment pdp:typeOfEnjambment ?enj_type.
            ?enj_type rdfs:label ?type_of_enjambment.
        }

    OPTIONAL{
        ?line pdp:hasMetricalSyllable ?met_syll.
        ?met_syll pdp:isStressed ?is_stressed_m;
            pdp:metricalSyllableNumber ?met_syll_number;
            pdp:phoneticTranscription ?met_syll_text.
    }

    OPTIONAL{
        ?line pdp:hasPunctuation ?punctuation.
        ?punctuation pdp:content ?punctuation_content.
        OPTIONAL{
            ?punctuation pdp:before ?before_word.
            ?before_word pdp:wordNumber ?before_word_number.
        }
        OPTIONAL{
            ?punctuation pdp:after ?after_word.
            ?after_word pdp:wordNumber ?after_word_number.
        }
    }

    OPTIONAL{
        ?line pdp:presentsRhyme ?rhyme.
        ?rhyme pdp:rhymeLabel ?rhyme_label.
    }

    OPTIONAL{
        ?line pdp:isEchoLineIn ?rhymeMatch_echo.
        ?rhymeMatch_echo pdp:rhymeGrapheme ?rhyme_grapheme_echo;
            pdp:typeOfRhymeMatching ?rmte;
            pdp:hasCallLine ?call_line.
        ?rmte rdfs:label ?rhyme_matching_type_echo.
        ?call_line pdp:absoluteLineNumber ?call_line_number.
    }

    OPTIONAL{
        ?line pdp:isCallLineIn ?rhymeMatch_call.
        ?rhymeMatch_call pdp:rhymeGrapheme ?rhyme_grapheme_call;
            pdp:typeOfRhymeMatching ?rmtc;
            pdp:hasEchoLine ?echo_line.
        ?rmtc rdfs:label ?rhyme_matching_type_call.
        ?echo_line pdp:absoluteLineNumber ?echo_line_number.
    }

    OPTIONAL{
        ?line pdp:patterningMetricalScheme ?patterning_metrical_scheme.
    }

    OPTIONAL{
        ?stanza pdp:rhymeScheme ?stanza_type.
    }

    OPTIONAL{
        ?gram_syll pdp:isFirstGrammaticalSyllableAffectedBy ?metaplasm.
        ?metaplasm pdp:typeOfMetaplasm ?tom.
        ?tom rdfs:label ?type_of_metaplasm.
        OPTIONAL{
            ?metaplasm pdp:metaplasmIndex ?metaplasm_index.
        }
    }
}    
    '''
}

CONTEXT_QUERY = {
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
    "patterningMetricalScheme": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#patterningMetricalScheme"},
    "rhymeScheme": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#rhymeScheme"},
    "relativeLineNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#relativeLineNumber"},
    "absoluteLineNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#absoluteLineNumber"},
    "hasPunctuation": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasPunctuation",
                       "@type": "@id",
                       "@container": "@set"},
    "isRealisedThrough": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#isRealisedThrough"},
    "text": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#text"},
    "metricalSyllableList": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasMetricalSyllable",
                            "@type": "@id",
                            "@container": "@set"},
    "wordList": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasWord",
                "@type": "@id",
                "@container": "@set"},
    "grammaticalSyllableList": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasGrammaticalSyllable",
                                "@type": "@id",
                                "@container": "@set"},
    "grammaticalSyllableNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#grammaticalSyllableNumber"},
    "metricalSyllableNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#metricalSyllableNumber"},
    "isStressed": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isStressed"},
    "analysesWord": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#analysesWord",
                     "@type": "@id",
                     "@container": "@set"},
    "isGrammaticalSyllableAnalysedBy": {"@id":"http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isGrammaticalSyllableAnalysedBy",
                                        "@container": "@set"},
    "isMetricalSyllableAnalysedBy": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isMetricalSyllableAnalysedBy",
                                     "@type": "@id",
                                     "@container": "@set"},
    "content": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#content"},
    "wordNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#wordNumber"},
    "scansions": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#scansions"},
    "typeOfScansion": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#typeOfScansion"},
    "employedTechnique": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#employedTechnique",
                          "@type": "@id"},
    "lineList": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#lineList",
                 "@container": "@set"},
    "stanzaList": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#stanzaList",
                   "@container": "@set"},
    "stanzaNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#stanzaNumber"},
    "typeOfRhymeMatching": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#typeOfRhymeMatching"},
    "rhyme": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#rhyme"},
    "rhymeLabel": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#rhymeLabel"},
    "isWordAnalysedBy": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isWordAnalysedBy",
                         "@type": "@id",
                         "@container": "@set"},
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
    "before": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#before",
               "@type": "@id"},
    "after": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#after",
               "@type": "@id"},
    "hasRhymeMatch": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasRhymeMatch",
                "@type": "@id",
                "@container": "@set"},
    "hasEchoLine": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasEchoLine",
                "@type": "@id"},
    "hasCallLine": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasCallLine",
                "@type": "@id"},
    "rhymeGrapheme": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#rhymeGrapheme"},
    "hasEchoWord": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasEchoWord",
                "@type": "@id"},
    "hasCallWord": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasCallWord",
                "@type": "@id"},
    "presentsRhyme":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#presentsRhyme",
                "@type": "@id"},
    "isRhymePresentAt": { "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isRhymePresentAt",
        "@type": "@id"},
    "isLineAffectedBy": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isLineAffectedBy",
        "@type": "@id"},
    "isFirstWordAffectedBy":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isFirstWordAffectedBy",
        "@type": "@id"},
    "id": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#id"},
    "isCallLineIn": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isCallLineIn",
                "@type": "@id"},
    "isEchoLineIn": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isEchoLineIn",
                "@type": "@id"},
    "isFirstGrammaticalSyllableAffectedBy": {
            "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isFirstGrammaticalSyllableAffectedBy",
            "@type": "@id"
    },
    "beforeWordNumber": {
            "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#beforeWordNumber"
    },
    "afterWordNumber": {
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#afterWordNumber"
    },
    "callLineNumber":{
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#callLineNumber"
    },
    "echoLineNumber":{
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#echoLineNumber"
    },
    "metaplasms":{
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isFirsGrammaticalSyllableAffectedBy",
    },
    "metaplasmIndex":{
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#metaplasmIndex",
        "@type": "http://www.w3.org/2001/XMLSchema#nonNegativeInteger"
    },
    "metricalType":{"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#metricalType"},
    "grammaticalStressPattern": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#grammaticalStressPattern"},
    "syllabicMetricalLength": {
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#syllabicMetricalLength"},
    "lineMaxLength": {
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#lineMaxLength"},
    "lineMinLength": {
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#lineMinLength"}

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
                "@type": "@id",
                "@container": "@set"},
    "lines": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasLine",
                "@type": "@id",
                "@container": "@set"},
    "redactionPattern": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasRedactionPattern"},
    "stanzaPattern": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasStanzaPattern"},
    "linePattern": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasLinePattern"},
    "patterningMetricalScheme": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#patterningMetricalScheme"},
    "rhymeScheme": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#rhymeScheme"},
    "relativeLineNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#relativeLineNumber"},
    "absoluteLineNumber": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#absoluteLineNumber"},
    "hasPunctuation": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#hasPunctuation",
                       "@type": "@id"},
    "metricalType": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#metricalType",
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
                    "@type": "@id"},
    "scansion_id": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#graphName",
                    "@type": "@id"},
    "isCallLineIn": {
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isCallLineIn",
        "@type": "@id"},
    "isEchoLineIn": {
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isEchoLineIn",
        "@type": "@id"},
    "isLineAffectedBy": {
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#isLineAffectedBy",
        "@type": "@id"},
    "presentsRhyme": {
        "@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#presentsRhyme",
        "@type": "@id"},
    "hasAgent": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-core#hasAgent"},
    "syllabicMetricalLength": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#syllabicMetricalLength"},
    "lineMaxLength": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#lineMaxLength"},
    "lineMinLength": {"@id": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#lineMinLength"}
}
