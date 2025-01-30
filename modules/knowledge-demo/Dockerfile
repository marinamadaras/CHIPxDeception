FROM ontotext/graphdb:10.6.3

# Copy over data
COPY data /data

# Copy over entrypoint
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]