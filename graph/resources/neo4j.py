from neo4j import GraphDatabase, basic_auth


driver = GraphDatabase.driver(
  "bolt://localhost:7687",
  auth=basic_auth("neo4j", "TO_CHANGE")) # Username: "neo4j" by default, Password: "pass4database"

imdb = pd.read_csv('/Users/egomez/Downloads/imdb.csv')
#imdb.head()

# Cypher query to write nodes and relationships into DB
cypher_query = '''
    MERGE (m:Movie {id: $id, title: $title, year: $year, rating: $rating, votes: $votes})
    MERGE (d:Director {name: $director})
    MERGE (d)-[:HAS_DIRECTED]->(m)
    MERGE (a1:Actor {name: $star1})
    MERGE (a2:Actor {name: $star2})
    MERGE (a3:Actor {name: $star3})
    MERGE (a4:Actor {name: $star4})
    MERGE (a1)-[:HAS_ACTED_IN]->(m)
    MERGE (a2)-[:HAS_ACTED_IN]->(m)
    MERGE (a3)-[:HAS_ACTED_IN]->(m)
    MERGE (a4)-[:HAS_ACTED_IN]->(m)
'''

# Function that runs the query by passing some properties
def create_movie(tx, id, title, year, rating, votes, director, star1, star2, star3, star4):
    tx.run(cypher_query, id = id, title = title, year = year, rating = rating, votes = votes, director = director,
          star1 = star1, star2 = star2, star3 = star3, star4 = star4)

# Open connection with DB, loop over the DataFrame's rows and write nodes/relationships into DB
with driver.session(database="neo4j") as session:
    for i, row in imdb.iterrows():
        id = i
        title = row['Series_Title']
        year = row['Released_Year']
        rating = row['IMDB_Rating']
        votes = row['No_of_Votes']
        director = row['Director']
        star1 = row['Star1']
        star2 = row['Star2']
        star3 = row['Star3']
        star4 = row['Star4']
        session.write_transaction(create_movie, id, title, year, rating, votes, director,
                                  star1, star2, star3, star4)

driver.close()


cypher_query = '''
MATCH (m:Movie)
RETURN m.title, m.votes, m.rating
ORDER BY m.votes DESC
LIMIT 10
'''
def get_result(tx):
    result = tx.run(cypher_query).data() # .data() allows to retrieve the result as a list of dictionaries
    return result

# Open connection with DB, execute transaction and get results as a pandas dataframe
with driver.session(database="neo4j") as session:
    res = session.read_transaction(get_result) # here it's a read-only transaction
driver.close()
res = pd.DataFrame(res)
res
