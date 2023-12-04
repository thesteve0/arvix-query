from InstructorEmbedding import INSTRUCTOR
import numpy as np
from qdrant_client import QdrantClient
import time



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


sentence = "ocean red tide"
instruction  = "Represent the Research Paper abstract for retrieval; Input:"

t1 = time.perf_counter(), time.process_time()
embeddings = model.encode([[instruction,sentence]])

t2 = time.perf_counter(), time.process_time()
print("\nCalculating embedding time")
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")


#print("embeddings: " + str(embeddings[0][:5]))

print("Similar search for " + "'sentence'")

client = QdrantClient("localhost", port=6333)
search_result = client.search(
    collection_name="arvix_abs",
    query_vector=embeddings[0],
    limit=10
)
# print(search_result)
for scored_result in search_result :
    print("Abstract: " + scored_result.payload["abstract"][:200] +"\n")

print("-----------------------------------------------------------------")
print("Dissimilar search for " + "'sentence'")
dissimilar_search_result = client.search(
    collection_name="arvix_abs",
    query_vector=-1*embeddings[0],
    limit=10
)

for scored_result in dissimilar_search_result :
    print("Abstract: " + scored_result.payload["abstract"][:200] +"\n")

print("finished")