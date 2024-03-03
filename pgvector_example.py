import numpy as np
from pgvector.psycopg import register_vector
import psycopg

# generate random data
rows = 100000
dimensions = 128
embeddings = np.random.rand(rows, dimensions)
categories = np.random.randint(100, size=rows).tolist()
queries = np.random.rand(10, dimensions)

DB_NAME= 'pgvector_citus'

#Make the table
conn = psycopg.connect("host=localhost user=postgres password='letmein'", autocommit=True)
cursor = conn.cursor()

cursor.execute("SELECT datname FROM pg_database;")

list_database = cursor.fetchall()

if ('pgvector_citus',) in list_database:
    cursor.execute(("DROP database "+ DB_NAME +" with (FORCE);"))
    cursor.execute("create database " + DB_NAME + ";");
else:
    cursor.execute("create database " + DB_NAME + ";");

#Now close the connection and switch DB
conn.close()


# enable extensions
conn = psycopg.connect("host=localhost user=postgres password='letmein' dbname='pgvector_citus'", autocommit=True)
conn.execute('CREATE EXTENSION IF NOT EXISTS vector')

# GUC variables set on the session do not propagate to Citus workers
# https://github.com/citusdata/citus/issues/462
# you can either:
# 1. set them on the system, user, or database and reconnect
# 2. set them for a transaction with SET LOCAL
# S
conn.close()

# reconnect for updated GUC variables to take effect
conn = psycopg.connect("host=localhost user=postgres password='letmein' dbname='pgvector_citus'", autocommit=True)
register_vector(conn)

print('Creating distributed table')
conn.execute('DROP TABLE IF EXISTS items')
conn.execute('CREATE TABLE items (id bigserial, embedding vector(%d), category_id bigint, PRIMARY KEY (id, category_id))' % dimensions)
#conn.execute('SET citus.shard_count = 4')
#conn.execute("SELECT create_distributed_table('items', 'category_id')")

print('Loading data in parallel')
with conn.cursor().copy('COPY items (embedding, category_id) FROM STDIN WITH (FORMAT BINARY)') as copy:
    copy.set_types(['vector', 'bigint'])

    for i in range(rows):
        copy.write_row([embeddings[i], categories[i]])

conn.close()

# print('Creating index in parallel')
# conn.execute('CREATE INDEX ON items USING hnsw (embedding vector_l2_ops)')
#
# print('Running distributed queries')
# for query in queries:
#     items = conn.execute('SELECT id FROM items ORDER BY embedding <-> %s LIMIT 10', (query,)).fetchall()
#     print([r[0] for r in items])