from collections import Counter
import psycopg
from pgvector.psycopg import register_vector
from InstructorEmbedding import INSTRUCTOR



### The purpose of this code is to demonstrate use PostgreSQL Full Text search alongside vector search (sparse vs
## dense vectors). This file assumes you have already imported the Arxiv data and built the HNSW index on the vector using
### cosine distance

### https://www.postgresql.org/docs/current/textsearch-tables.html#TEXTSEARCH-TABLES-SEARCH
### https://www.postgresql.org/docs/current/textsearch-controls.html
### https://www.postgresql.org/docs/current/textsearch-features.html#TEXTSEARCH-MANIPULATE-TSQUERY

DB_NAME = "arxiv_abstracts"

connect_string = f"host=localhost user=postgres password='letmein' dbname='{DB_NAME}'"

sentence_list = ["simulated", "annealing"]

tsquery_text = f"to_tsquery('english','{sentence_list[0]} & {sentence_list[1]}')"

sql = "select id, ts_rank_cd(to_tsvector(abstract), " +  tsquery_text + (") as rank,  abstract "
        "from documents where to_tsvector( abstract) @@ " + tsquery_text + "order by rank DESC limit 40")

conn = psycopg.connect(connect_string, autocommit=True)
register_vector(conn)

# Create the ful text index
conn.execute('CREATE INDEX IF NOT EXISTS arxiv_abstract_fulltext_idx ON documents USING GIN (to_tsvector(\'english\', abstract))')

# Now do a full text search
# https://www.postgresql.org/docs/current/functions-textsearch.html
results = conn.execute(sql).fetchall()

print("-----------------------------------------------------------------\n")
print("Similar search for " + str(sentence_list) + "\n")
print("-----------------------------------------------------------------\n")

for result in results:
    print("id: " + str(result[0]) + " || rank: " +  str(result[1]) + " || abstract: " + result[2][:50])

############## Now a hybrid search ###############
### Reciprocal Rank Fusion (RRF) for combining full-text and vectors
### https://safjan.com/implementing-rank-fusion-in-python/

#gather 10 vector results
sentence = "simulated annealing"
instruction  = "Represent the Research Paper abstract for retrieval; Input:"
model = INSTRUCTOR('hkunlp/instructor-xl')


embeddings = model.encode([[instruction,sentence]])
query_embedding = embeddings[0]
results_dense = conn.execute('SELECT id, (embedding <=> %s) as distance, abstract FROM documents ORDER BY embedding <=> %s LIMIT 40', (query_embedding, query_embedding, )).fetchall()

# turn each results in hashes
sparse_scores = {}
dense_scores = {}

for i in range(len(results)):
    score = 1/(30 + i)
    sparse_scores[results[i][0]] = score
    dense_scores[results_dense[i][0]] = score

mixed_scores = dict(Counter(sparse_scores) + Counter(dense_scores))
mixed_scores_sorted = dict(sorted(mixed_scores.items(), key=lambda key_val: key_val[1], reverse=True))

print("We had " + str(80 - len(mixed_scores_sorted)) + "results overlap")
for k,v in mixed_scores_sorted.items():
    print("ID: " + str(k) + " score: " + str(v) )

print("finished")
