# Italian-lyrics-retrieval-system

In the following repository, various aspects contributing to the development of the ["Italian Lyrics Retrieval System"](https://nlp.stanford.edu/IR-book/information-retrieval-book.html) are examined and explored. Among the implemented concepts, methods for document preprocessing, duplicate removal, compression, result classification, handling of phrase queries, and a brief analysis of the phonetic algorithms used are highlighted.

Disclaimer: The following repository is not intended as a detailed guide on algorithm implementations; for these details, please refer to the book [”Introduction to Information Retrieval"](https://nlp.stanford.edu/IR-book/information-retrieval-book.html). Alongside the text, a possible and simple implementation of the system in Python is provided.

## Modules:

In this repository different concepts of the information retrieval can be retrieved.
- preprocessing
- simhash duplicates removal
- compression techniques
- index construction (boolean and positional)
- queries retrieval (boolean, tf-idf, okapi-bm25, phrase queries)

## Environment
`conda create -n <env_name> python=3.9` <br>
`conda activate <env_name>` <br>
`pip install -r requirements.txt` <br>
`pip install lingua==4.15.0` <br>
`pip install lingua-language-detector==2.0.2`

## Examples

The indexes for the examples are provided within this repository. If you want the entire colletion is available [here](https://drive.google.com/file/d/1xqAqqUhJ9juD3uGtEVdxZi2gp-JWgjuZ/view?usp=share_link).