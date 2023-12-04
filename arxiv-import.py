# @TODO
# This script needs to import the arvix parquets into the postgres instance and creates th index

### DO NOT USE = this is my failed attempt to try to get the data into pgvector

import re
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import psycopg
from pgvector.psycopg import register_vector
from pathlib import Path

# The proper word is arxiv but I messed when creating the folder and project

PARQUET_PATH= Path('../arvix_abstracts/arxiv_abstracts')
DB_NAME= 'arxiv'

conn = psycopg.connect("host=127.0.0.1 user=postgres password='test'", autocommit=True)
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
conn = psycopg.connect("host=127.0.0.1 user=postgres password='test' dbname='arxiv' ")
cursor = conn.cursor()


cursor.execute('CREATE EXTENSION IF NOT EXISTS vector')
register_vector(conn)
cursor.execute('CREATE TABLE documents (id bigserial PRIMARY KEY, abstract text, embedding vector(768))')
cursor.connection.commit()

for path in PARQUET_PATH.rglob('*.parquet'):
    match = re.search('.*(\w{16})\.parquet', str(path))
    data_table = pa.parquet.read_table(path, memory_map=True, columns=['abstract', 'embeddings'])
    data_pandas = data_table.to_pandas()
    #cursor.executemany("INSERT INTO documents (abstract, embedding) VALUES (%s, %s)", data_table.to_pylist())
    print("working on: " + str(path))
    i = 0
    # for idx, row in data_pandas.iterrows():
    #     abstract = row['abstract']
    #     embedding = row['embeddings']
    #     cursor.executemany("INSERT INTO documents (abstract, embedding) VALUES (%s, %s)", (abstract, embedding.tolist()))
    #     if (i % 1000 == 0):
    #         print("working on row: " + str(i))
    #     i = i + 1
    # cursor.connection.commit()


    with cursor.copy("COPY documents (abstract, embedding) FROM STDIN") as copy:
            print("working on: " + str(path))
            i = 0
            for item in data_table.to_pylist():
                print("working on row: " + str(i))
                abstract = item['abstract']
                embedding = item['embeddings']
                item_tuple = (abstract, embedding)
                copy.write_row(item_tuple)
                i = i + 1
    cursor.connection.commit()
        #cursor.mogrify("INSERT INTO documents (abstract, embedding) VALUES (%s, %s)", (abstract, embedding.tolist()))
        #cursor.execute("INSERT INTO documents (abstract, embedding) VALUES (%s, %s)", (abstract, embedding.tolist()))
        #print(" ")
    # for row in data:
    #     abstract = data['abstract']
    #     embedding = data['embeddings']



    #print(item)
    # data['embeddings'][1]
    # conn.execute('INSERT INTO documents (content, embedding) VALUES (%s, %s)', (content, embedding))
    # print("RSS: {}MB".format(pa.total_allocated_bytes() >> 20))
    #print(path)
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