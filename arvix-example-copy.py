from pgvector.psycopg import register_vector
import psycopg
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq

PARQUET_PATH = Path('./')
DB_NAME= 'arxiv2'
data_pandas = 'replaced later'
dimensions = 768

# NOTE: The only works for a single file bc we read the file and then copy it
# This won't work when there are many parquet files in the directory
for path in PARQUET_PATH.glob('*.parquet'):
    print("working on: " + str(path))
    data_table = pa.parquet.read_table(path, memory_map=True)
    data_pandas = data_table.to_pandas()



#Make the table
conn = psycopg.connect("host=localhost user=postgres password='letmein'", autocommit=True)
cursor = conn.cursor()

cursor.execute("SELECT datname FROM pg_database;")

list_database = cursor.fetchall()

if ('arxiv2',) in list_database:
    cursor.execute(("DROP database "+ DB_NAME +" with (FORCE);"))
    cursor.execute("create database " + DB_NAME + ";");
else:
    cursor.execute("create database " + DB_NAME + ";");

#Now close the connection and switch DB
conn.close()

# enable extensions
conn = psycopg.connect("host=localhost user=postgres password='letmein' dbname='pgvector_citus'", autocommit=True)
conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
conn.close()
# reconnect for updated GUC variables to take effect
conn = psycopg.connect("host=localhost user=postgres password='letmein' dbname='pgvector_citus'", autocommit=True)
register_vector(conn)

print('Creating distributed table')
conn.execute('DROP TABLE IF EXISTS items')
conn.execute('CREATE TABLE items (id bigserial, embedding vector(%d), abstract text, PRIMARY KEY (id))' % dimensions)


print('Loading data in parallel')
with conn.cursor().copy('COPY items ( embedding,abstract) FROM STDIN WITH (FORMAT BINARY)') as copy:
    copy.set_types(['vector', 'text'])

    for i in range(11):
        copy.write_row([data_pandas.iloc[i]["embeddings"], data_pandas.iloc[i]["abstract"]])

# print('Creating index in parallel')
# conn.execute('CREATE INDEX ON items USING hnsw (embedding vector_l2_ops)')
#
# print('Running distributed queries')
# for query in queries:
#     items = conn.execute('SELECT id FROM items ORDER BY embedding <-> %s LIMIT 10', (query,)).fetchall()
#     print([r[0] for r in items])