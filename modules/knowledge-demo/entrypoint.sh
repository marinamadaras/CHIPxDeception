#!/bin/bash

# curl -F config=@/data/repo-config.ttl localhost:7200/rest/repositories
/opt/graphdb/dist/bin/importrdf preload -f -c /data/repo-config.ttl /data/userKG_inferred_stripped.rdf
/opt/graphdb/dist/bin/graphdb -Dgraphdb.external-url=http://localhost:9000/kgraph/
