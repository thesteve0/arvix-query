# This is from the original file found here:
# https://alex.macrocosm.so/download

from InstructorEmbedding import INSTRUCTOR
import time
from pgvector.psycopg import register_vector
import psycopg

DB_NAME = "arxiv_abstracts"

connect_string = f"host=localhost user=postgres password='letmein' dbname='{DB_NAME}'"

#model = INSTRUCTOR('hkunlp/instructor-xl').cuda()
model = INSTRUCTOR('hkunlp/instructor-xl')

# CHANGE "sentence" HERE FOR DIFFERENT RESULTS
# read this to see examples of Instructor for information retrieval
# https://pypi.org/project/InstructorEmbedding/#use-customized-embeddings-for-information-retrieval
sentence = "Thames river pollution england"
instruction  = "Represent the Research Paper abstract for retrieval; Input:"

embeddings = model.encode([[instruction,sentence]])
query_embedding = embeddings[0]

print("-----------------------------------------------------------------\n")
print("Similar search for " + sentence + "\n")
print("-----------------------------------------------------------------\n")

conn = psycopg.connect(connect_string, autocommit=True)
register_vector(conn)

results = conn.execute('SELECT id, (embedding <=> %s) as distance, abstract FROM documents ORDER BY embedding <=> %s LIMIT 10', (query_embedding, query_embedding, )).fetchall()

for result in results:
    print("id: " + str(result[0]) + " || distance: " +  str(result[1]) + " || abstract: " + result[2][:50])


print("-----------------------------------------------------------------\n")
print("Dissimilar search for " + sentence + "\n")
print("-----------------------------------------------------------------\n")

dissimilar_embedding = -1 * query_embedding

results = conn.execute('SELECT id, (embedding <=> %s) as distance, abstract FROM documents ORDER BY embedding <=> %s LIMIT 10', (dissimilar_embedding, dissimilar_embedding, )).fetchall()

for result in results:
    print("id: " + str(result[0]) + " || distance: " +  str(result[1]) + " || abstract: " + result[2][:50])


print("finished")