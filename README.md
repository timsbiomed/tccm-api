## Getting Started with Docker

```
cd docker; docker-compose up
```


### Loader

Extract the skos-based RDF of ConceptReferences from OWL. 

```
robot query --input <ontology.owl> --query <sparql.rq> <turtle.ttl>
```