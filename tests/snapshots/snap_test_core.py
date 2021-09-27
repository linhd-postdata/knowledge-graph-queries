# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_get_authors 1'] = {
    'TODO': '''
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
