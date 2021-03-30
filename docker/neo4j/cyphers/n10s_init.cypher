CALL n10s.graphconfig.init();

DROP CONSTRAINT n10s_unique_uri IF EXISTS;
CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;

CALL n10s.graphconfig.init({
  handleVocabUris: 'MAP'
});


CALL n10s.nsprefixes.addFromText("
@prefix neo4voc: <http://neo4j.org/vocab/sw#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix termci: <https://hotecosystem.org/termci/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix biolinkml: <https://w3id.org/biolink/biolinkml/> .
");


// Node
call n10s.mapping.add('http://ww.w3.org/2004/02/skos/core#Concept', 'ConceptReference');
call n10s.mapping.add('http://www.w3.org/2004/02/skos/core#ConceptScheme', 'ConceptSystem');
call n10s.mapping.add('http://www.w3.org/2004/02/skos/core#CodeSet', 'CodeSet');

// Object Properties
call n10s.mapping.add('http://www.w3.org/2004/02/skos/core#broader', 'narrower_than');
call n10s.mapping.add('http://www.w3.org/2004/02/skos/core#inScheme', 'defined_in');
call n10s.mapping.add('http://www.w3.org/2004/02/skos/core#member', 'has_member');

// Data Type Properties
call n10s.mapping.add('http://www.w3.org/2004/02/skos/core#notation', 'code');
call n10s.mapping.add('http://www.w3.org/2004/02/skos/core#prefLabel', 'designation');
call n10s.mapping.add('http://www.w3.org/2004/02/skos/core#definition', 'definition');
call n10s.mapping.add('http://www.w3.org/2000/01/rdf-schema#seeAlso', 'reference');
