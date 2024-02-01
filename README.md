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
`git clone` <br>
`conda create -n <env_name> python=3.9` <br>
`conda activate <env_name>` <br>
`pip install -r requirements.txt` <br>
`pip install lingua==4.15.0` <br>
`pip install lingua-language-detector==2.0.2`

## Examples

The indexes for the examples are provided within this repository. If you want the entire colletion is available [here](https://drive.google.com/file/d/1xqAqqUhJ9juD3uGtEVdxZi2gp-JWgjuZ/view?usp=share_link).

To test the system just run the main file:

`python src/main.py`

Then follow the command line information to perform different queries. The queries can be perform on 3 different indexes:
- author (boolean) index
- title (boolean) index
- lyrics (positional) index

For the lyrics queries 2 types of query can be perfomed:
- keywords queries: specify some keywords and the system will compute the okapi-bm25 score (also the tf-idf can be used)
- phrase queries: specify a phrase queries in this way "This is a phrase query". Be carefull the system should get at least 2 tokens (NOT WORDS!) because some preprocessing are performed ("I am Carlo") this phrase contains only one token.

The system has been developed solely for informational purposes and may contain errors or unhandled exceptions. The use of parts of the system requires further scrutiny, and the best efficiency is not guaranteed. 