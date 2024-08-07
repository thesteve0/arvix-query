import re
import pyarrow as pa
import pyarrow.parquet as pq
import psycopg
from pgvector.psycopg import register_vector
from pathlib import Path

# The proper word is arxiv but I messed when creating the folder and project

PARQUET_PATH= Path('./')
DB_NAME= 'images'

conn = psycopg.connect("host=localhost user=postgres password='letmein'", autocommit=True)
cursor = conn.cursor()

cursor.execute("SELECT datname FROM pg_database;")

list_database = cursor.fetchall()

if (DB_NAME,) in list_database:
    cursor.execute(("DROP database "+ DB_NAME +" with (FORCE);"))
    cursor.execute("create database " + DB_NAME + ";")
else:
    cursor.execute("create database " + DB_NAME + ";")

#Now close the connection and switch DB
conn.close()

connect_string = f"host=localhost user=postgres password='letmein' dbname='{DB_NAME}'"

conn = psycopg.connect(connect_string,  autocommit=True)
conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
conn.close()

conn = psycopg.connect(connect_string, autocommit=True)
register_vector(conn)

conn.execute('DROP TABLE IF EXISTS documents')
conn.execute('CREATE TABLE documents (id bigserial PRIMARY KEY, abstract text, embedding vector(768))')

for path in PARQUET_PATH.glob('*.parquet'):
    match = re.search('.*(\w{16})\.parquet', str(path))
    data_table = pa.parquet.read_table(path, memory_map=True, columns=['abstract', 'embeddings'])
    data_pandas = data_table.to_pandas()

    print("working on: " + str(path))

    with conn.cursor().copy("COPY documents (embedding, abstract) FROM STDIN with (FORMAT BINARY)") as copy:
        print("working on: " + str(path))
        copy.set_types(['vector', 'text'])
        for i in range (0,len(data_pandas)):
        #for i in range(11):
            copy.write_row([data_pandas.iloc[i]["embeddings"], data_pandas.iloc[i]["abstract"]])


print('finished')
