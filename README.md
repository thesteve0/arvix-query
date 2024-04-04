# Arvix Query

There is a typo in the project which I kept here as well. It is not Arvix it is Arxiv. 

Caveat: This is not production level code. It was written to make teaching easy - there are a bunch of bad practices 
used. **PLEASE** do not copy and paste this directly

Here is the Arxiv site:
http://arxiv.org/

Original Data is here:
https://alex.macrocosm.so/download

We load one of the parquet files from here. The original file containing all the abstracts was 6.8GB. This smaller file is 
enough to demonstrate the concept (it is only 340MB):
https://github.com/thesteve0/arvix-query/releases/download/0.1/abstracts_1.parquet

Then use *arxiv-import.py* to import from the parquet file. Make sure to update connections parameters as needed

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