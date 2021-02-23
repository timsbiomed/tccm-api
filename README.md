## Getting Started with Docker

```
cd docker; docker-compose up
```


### Loader

Extract the skos-based RDF of ConceptReferences from OWL. 

```
robot query --input <ontology.owl> --query <sparql.rq> <turtle.ttl>
```

### Import file to neo4j

1. Create an RDF graph and export it to turtle. 

2. Put the ttl file in neo4j import directory

3. run this command

```
CALL n10s.rdf.import.fetch("file://import/<file_name>", "Turtle")
```

### DotEnv files

The `.env` file in the root directory is used only when running locally. The docker containers use the `.env`
file in the docker directory