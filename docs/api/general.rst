
General API Notes
=================

If one of the backend services (Neo4j, Elasticsearch) is unavailable,
a 503 error will be returned instead of a JSON response:

:statuscode 503: Service unavailable
