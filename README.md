# Arvix Query

Original Data not in qdrant format is here:
https://alex.macrocosm.so/download

Got the Qdrant database snapshot from here:

https://deploy-preview-199--condescending-goldwasser-91acf0.netlify.app/documentation/datasets/

This is how you upload the snapshot to Qdrant Server
```
curl -X POST 'http://127.0.0.1:6333/collections/COLLECTION_NAME/snapshots/upload' \
-H 'Content-Type:multipart/form-data' \
-F 'snapshot=@./arxiv_abstracts-3083016565637815127-2023-06-02-07-26-29.snapshot'
```

Data was originally encoded using this model
https://huggingface.co/hkunlp/instructor-xl

Here is the instruction and sentence needed for the Instructor embedding. Change the sentence to look for other terms or phrases

```python
sentence = "habitat corridors"
instruction  = "Represent the Research Paper abstract for retrieval; Input:"
```

Trying to get some Postgres working

`$ docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres`

`podman run -d -p 5432:5432 -e POSTGRES_PASSWORD=test --name maybe ghcr.io/thesteve0/pg16-full` 

