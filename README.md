# Arvix Query
The Alexindria project embedded all the abstract in Arxiv. They used the InstructorXL model to encode the text. This is a snapshot of the contents in the past.
They took the embeddings along with the original content and put it in a parquet files. The complete data with all the abstracts is 6.8GB, which is impractical 
for this workshop. Instead we are just going to use one of the parquet files (340MB).

## Steps to get ready
1. We run the arxiv import.py which will create the table with the pg_vector extension and then move the data into the database
2. We need to run the SQL commands in sql_commands.sql to create the HNSW index
3. Now you can run a straight vector similary search using arxiv-vector-query. There are multiple types of queries in that file and you can change the abstract text you are sending
4. arxiv-hybrid-query combines the results from PostgreSQL full text search and a pg_vector search to provide a combination of similarity and exact word search 


There is a typo in the project which I kept here as well. It is not Arvix it is Arxiv. 

Caveat: This is not production level code. It was written to make teaching easy - there are a bunch of bad practices 
used. **PLEASE** do not copy and paste any of this directly into your production code

Here is the Arxiv site:
http://arxiv.org/

Original Data is here:
https://alex.macrocosm.so/download

We load one of the parquet files from here. The original file containing all the abstracts was 6.8GB. This smaller file is 
enough to demonstrate the concept (it is only 340MB):
https://github.com/thesteve0/arvix-query/releases/download/0.1/abstracts_1.parquet

Then use *arxiv-import.py* to import from the parquet file. Make sure to update connections parameters as needed

After import we need to run the commands in sql_commands.sql to build the index

Data was originally encoded using this model
https://huggingface.co/hkunlp/instructor-xl

Here is the instruction and sentence needed for the Instructor embedding. Change the sentence to look for other abstracts
with similar content



```python
sentence = "habitat corridors"
instruction  = "Represent the Research Paper abstract for retrieval; Input:"
```

This project requires a running Postgresql instance with the pgvector extension.  
https://github.com/pgvector/pgvector
