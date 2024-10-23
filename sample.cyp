MATCH (m:Movie {title:$movie})<-[:RATED]-(u:User)-[:RATED]->(rec:Movie) RETURN distinct rec.title AS recommendation LIMIT 20;
MATCH (m:Movie {title: $movie})<-[:DIRECTED]-(d:Director)-[:DIRECTED]->(rec:Movie) RETURN DISTINCT rec.title AS recommendation LIMIT 5;
MATCH (m:Movie {title: $movie})-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(rec:Movie)<-[:RATED]-(u:User) RETURN DISTINCT rec.title AS recommendation LIMIT 10;