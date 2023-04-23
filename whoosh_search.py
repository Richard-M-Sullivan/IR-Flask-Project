from whoosh.index import open_dir
from whoosh.qparser import QueryParser, OrGroup
from whoosh.query import *

# open the index, which stores all the values in the corpus
ix = open_dir("index")

print(ix.schema)
# build a query parser, so that we can make queries
or_group = OrGroup.factory(0.9)
qp = QueryParser("lyrics", schema=ix.schema, group=or_group)

# get user input to make queries
while True:
    query = input("make a query\n")
    if query.lower() == "quit":
        break
    
    q = qp.parse(query)

    with ix.searcher() as s:
        results = s.search(q)

        for i, result in enumerate(results):
            print()
            print(f'Song Result {i+1}')
            print(f'Title: {result["song"]}')
            print(f'Artist: {result["artist"]}')
            print(f'Year: {result["year"]} Rank: {result["rank"]}')
            

