-- we loaded the vectors, now we need to create the HNSW index on the table
-- Distance measure here has to match the distance metric in our query
-- https://aws.amazon.com/blogs/database/optimize-generative-ai-applications-with-pgvector-indexing-a-deep-dive-into-ivfflat-and-hnsw-techniques/
-- https://www.crunchydata.com/blog/hnsw-indexes-with-postgres-and-pgvector
-- https://jkatz05.com/post/postgres/distributed-pgvector/

select count(*) from documents;

-- distance metrics
-- https://aiven.io/developer/postgresql-pgvector-indexes
-- https://www.imaurer.com/which-vector-similarity-metric-should-i-use/
-- https://devcenter.heroku.com/articles/pgvector-heroku-postgres#perform-vector-queries
-- vector_l2_ops = L2 distance use <->
-- vector_cosine_ops = cosine distance use <=>
-- vector_ip_ops = inner product distance use

-- Remember HNSW index creation is memory HUNGRY

-- See how big the current working memory is
SELECT current_setting('work_mem');

-- 350MB should be able to handle all the records we imported
set maintenance_work_mem to '350MB';
CREATE INDEX idx_documents_hnsw ON documents USING hnsw
    (embedding vector_cosine_ops) WITH (m = 10, ef_construction = 40);

