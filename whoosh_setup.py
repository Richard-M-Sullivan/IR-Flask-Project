import os
import csv
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED

# Define schema for the index
schema = Schema(
        rank   = TEXT(stored=True),
        song   = TEXT(stored=True),
        artist = TEXT(stored=True),
        year   = TEXT(stored=True),
        lyrics = TEXT(stored=True),
        source = TEXT(stored=True))

# Create index directory if it does not exist
if not os.path.exists("index"):
    os.mkdir("index")

# Create the index and open it for writing
index = create_in("index", schema)

# Open the CSV file and read each row
with open("lyrics.csv", "r", encoding="ISO-8859-1") as f:
    reader = csv.DictReader(f)
    writer = index.writer()
    for i,row in enumerate(reader):
        print(i,row)
        # Add each row to the index
        writer.add_document(
            rank   = row["Rank"],
            song   = row["Song"],
            artist = row["Artist"],
            year   = row["Year"],
            lyrics = row["Lyrics"],
            source = row["Source"])

# Commit the changes to the index
writer.commit()

