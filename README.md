# Arvix Query

Got the data set from here:

https://deploy-preview-199--condescending-goldwasser-91acf0.netlify.app/documentation/datasets/

Data was originally encoded using this model
https://huggingface.co/hkunlp/instructor-xl

Here is the instruction and sentence needed for the Instructor embedding. Change the sentence to look for other terms or phrases

```python
sentence = "habitat corridors"
instruction  = "Represent the Research Paper abstract for retrieval; Input:"
```



Original Data not in qdrant format is here:
https://alex.macrocosm.so/download


`$ docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres`

`podman run -d -p 5432:5432 -e POSTGRES_PASSWORD=test --name maybe ghcr.io/thesteve0/pg16-full` 