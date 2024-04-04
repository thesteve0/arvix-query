import numpy as np
from InstructorEmbedding import INSTRUCTOR
import time
from pgvector.psycopg import register_vector
import psycopg

DB_NAME = "arxiv_abstracts"

connect_string = f"host=localhost user=postgres password='letmein' dbname='{DB_NAME}'"


# This is from the original file found here:
# https://alex.macrocosm.so/download

# from InstructorEmbedding import INSTRUCTOR
#
# model = INSTRUCTOR('hkunlp/instructor-xl')
# sentence = "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train."
# instruction = "Represent the Research Paper abstract for retrieval; Input:"
# embeddings = model.encode([[instruction,sentence]])
# print(embeddings)


t1 = time.perf_counter(), time.process_time()
#model = INSTRUCTOR('hkunlp/instructor-xl').cuda()
model = INSTRUCTOR('hkunlp/instructor-xl')
t2 = time.perf_counter(), time.process_time()
print("model load time")
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")


sentence = "The increase in red tide dinoflagellates off the coast of Florida"
instruction  = "Represent the Research Paper abstract for retrieval; Input:"

t1 = time.perf_counter(), time.process_time()

embeddings = model.encode([[instruction,sentence]])
query_embedding = embeddings[0]

t2 = time.perf_counter(), time.process_time()
print("\nCalculating embedding time")
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")

print("-----------------------------------------------------------------\n")
print("Similar search for " + sentence + "\n")
print("-----------------------------------------------------------------\n")

conn = psycopg.connect(connect_string, autocommit=True)
register_vector(conn)

results = conn.execute('SELECT (embedding <=> %s) as distance, abstract FROM documents ORDER BY embedding <=> %s LIMIT 5', (query_embedding, query_embedding, )).fetchall()

for result in results:
    print("distance: " + str(result[0]) + "\nabstract: " + result[1][:300])

print("-----------------------------------------------------------------\n")
print("Dissimilar search for " + sentence + "\n")
print("-----------------------------------------------------------------\n")

dissimilar_embedding = -1 * query_embedding

results = conn.execute('SELECT (embedding <=> %s) as distance, abstract FROM documents ORDER BY embedding <=> %s LIMIT 5', (dissimilar_embedding, dissimilar_embedding, )).fetchall()

for result in results:
    print("distance: " + str(result[0]) + "\nabstract: " + result[1][:300])


print("finished")