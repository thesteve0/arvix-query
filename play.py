from InstructorEmbedding import INSTRUCTOR
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


sentence = "The increase in red tide dinoflagellates off the coast of Florida"
instruction  = "Represent the Research Paper abstract for retrieval; Input:"

t1 = time.perf_counter(), time.process_time()

embeddings = model.encode([[instruction,sentence]])

t2 = time.perf_counter(), time.process_time()
print("\nCalculating embedding time")
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")

print("-----------------------------------------------------------------\n")
print("Similar search for " + sentence + "\n")
print("-----------------------------------------------------------------\n")

client = QdrantClient("localhost", port=6333)
search_result = client.search(
    collection_name="arvix_abs",
    query_vector=embeddings[0],
    limit=3
)

# Now just display the results
for scored_result in search_result :
    print("Abstract: " + scored_result.payload["abstract"][:400] +"\n")


print("-----------------------------------------------------------------\n")
print("Dissimilar search for " + sentence + "\n")
print("-----------------------------------------------------------------\n")

dissimilar_search_result = client.search(
    collection_name="arvix_abs",
    query_vector=-1*embeddings[0],
    limit=3
)

for scored_result in dissimilar_search_result :
    print("Abstract: " + scored_result.payload["abstract"][:400] +"\n")

print("finished")