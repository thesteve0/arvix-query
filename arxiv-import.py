# @TODO
# This script needs to import the arvix parquets into the postgres instance and creates th index

### DO NOT USE = this is my failed attempt to try to get the data into pgvector

import re
import sys

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import psycopg
from pgvector.psycopg import register_vector
from pathlib import Path

# The proper word is arxiv but I messed when creating the folder and project

PARQUET_PATH= Path('./')
DB_NAME= 'arxiv'

conn = psycopg.connect("host=localhost user=postgres password='letmein'", autocommit=True)
cursor = conn.cursor()

cursor.execute("SELECT datname FROM pg_database;")

list_database = cursor.fetchall()

if ('arxiv',) in list_database:
    cursor.execute(("DROP database "+ DB_NAME +" with (FORCE);"))
    cursor.execute("create database " + DB_NAME + ";");
else:
    cursor.execute("create database " + DB_NAME + ";");

#Now close the connection and switch DB
conn.close()

conn = psycopg.connect("host=127.0.0.1 user=postgres password='letmein' dbname='arxiv' ")
cursor = conn.cursor()


cursor.execute('CREATE EXTENSION IF NOT EXISTS vector')
register_vector(conn)

conn.execute('DROP TABLE IF EXISTS documents')
cursor.execute('CREATE TABLE documents (id bigserial PRIMARY KEY, abstract text, embedding vector(768))')
cursor.connection.commit()
#sys.exit()
## Loop through the parquet files)
for path in PARQUET_PATH.rglob('*.parquet'):
    match = re.search('.*(\w{16})\.parquet', str(path))
    data_table = pa.parquet.read_table(path, memory_map=True, columns=['abstract', 'embeddings'])
    data_pandas = data_table.to_pandas()
    #cursor.executemany("INSERT INTO documents (abstract, embedding) VALUES (%s, %s)", data_table.to_pylist())
    print("working on: " + str(path))
    i = 0



    with cursor.copy("COPY documents (abstract, embedding) FROM STDIN with (FORMAT BINARY)") as copy:
            print("working on: " + str(path))
            #for i in range(data_pandas.rows):
            for i in range(11):
                copy.write_row([data_pandas.abstract[i], data_pandas.embeddings[i]])

    #copy.set_types(['text', 'vector'])
            # i = 0
            # for item in data_table.to_pylist():
                # print("working on row: " + str(i))
                # abstract = item['abstract']
                # embedding = np.asarray(item['embeddings'])
                # # item_tuple = (abstract, embedding)
                # copy.write_row([abstract, embedding])
                i = i + 1
                if i == 11: break
conn.close()
print('finished')
# Should it create the DB and then load the vector extension - yes for now
# Table structure
# id autoincrementing int
# abstract text
# embedding vector
#
# Then build the hnsw index

# Load a parquet file - since they are so huge might have to do a 1:1 parquet table insert

# maybe format properly

# insert into postgres